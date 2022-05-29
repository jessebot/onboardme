#!/bin/bash

set -o nounset
set -o pipefail

#profile to use for demo (absolute path)
export DEMO_DIR="/home/max/onboardme/configs/ansible_profiles/basic_desktop"
export ANSIBLE_CONFIG=$(cat "/home/max/onboardme/ansible/config")

# shared files
export SYNCED_DIR=""
SYNCED_DIR=$(find "$(cd ..; pwd)" -name "synced_dir")

export_metatdata(){
  # VM Metatdata
  export IMAGE_TYPE="img" #img or iso
  export HOST_ADDRESS="192.168.50.100"
  export HOST_SSH_PORT="22"
  export VM_NAME="testvm"
  export VM_USER="vmadmin"
  export VM_SSH_PORT="1234"
  export DISK_NAME="boot.img"
  export DISK_SIZE="60G"
  export ISO_FILE="ubuntu-22.04-live-server-amd64.iso"
  export UBUNTU_CODENAME="jammy"
  export CLOUD_IMAGE_NAME="${UBUNTU_CODENAME}-server-cloudimg-amd64"
  export CLOUD_IMAGE_URL="https://cloud-images.ubuntu.com/jammy/current"
  export MEMORY="8G"
  export PHYSICAL_CORES="4"
  export VGA="std"
  export VM_KEY=""
  export VM_KEY_FILE="$VM_USER"

  # Ansible metadata
  export UUID="none"
  export INVENTORY_PATH="/home/max/onboardme/ansible/inventories"
  export ANSIBLE_INVENTORY_FILE="$VM_NAME/$VM_NAME-inventory.yaml"
  export ANSIBLE_PLAYBOOK="/home/max/onboardme/ansible/playbooks/main-program.yaml"

  #program verbosity
  export VERBOSITY="-v"
  export DEBUG="true"
  export SQUASH="false"
}

# create a directory to hold the VM assets
create_dir(){
  mkdir "$VM_NAME"
  cd "$VM_NAME"
  export UUID=$(uuidgen)
}

# download a cloud image as .img
download_cloud_image(){
  wget -c -O "$CLOUD_IMAGE_NAME".img \
  "$CLOUD_IMAGE_URL"/"$CLOUD_IMAGE_NAME".img
}

# Create and expanded image
expand_cloud_image(){
  qemu-img create -b ${CLOUD_IMAGE_NAME}.img -f qcow2 \
  	-F qcow2 ${CLOUD_IMAGE_NAME}-new.img \
  	"$DISK_SIZE"
}

# convert the .img to qcow2 to use as base layer
img_to_qcow(){
  qemu-img convert -f raw \
    -O qcow2 "$CLOUD_IMAGE_NAME"_original.img \
    "$CLOUD_IMAGE_NAME".qcow2
}

# create the next layer on the image
create_qcow_image(){
  qemu-img create -f qcow2 \
    -F qcow2 \
    -o backing_file="$CLOUD_IMAGE_NAME"_base.qcow2 \
    "$VM_NAME".qcow2
}

# create a ssh key for the user and save as a file w/ prompt
create_ssh_key(){
  ssh-keygen -C "$VM_USER" \
    -f "$VM_KEY_FILE" \
    -N '' \
    -t rsa

  VM_KEY_FILE=$(find "$(cd ..; pwd)" -name $VM_USER)
  VM_KEY=$(cat "$VM_KEY_FILE".pub)
}

# cloud-init logs are in /run/cloud-init/result.json
create_user_data(){
cat > user-data <<EOF
#cloud-config
#vim:syntax=yaml

cloud_config_modules:
 - runcmd

cloud_final_modules:
 - [users-groups, always]
 - [scripts-user, once-per-instance]

groups:
  - docker

users:
  - name: ${VM_USER}
    groups: docker, admin, sudo, users
    shell: /bin/bash
    sudo: [ "ALL=(ALL) NOPASSWD:ALL" ]
    ssh-authorized-keys:
      - ${VM_KEY}
EOF
}

# create a disk
create_virtual_disk(){
  qemu-img create -f qcow2 \
    -F qcow2 \
    -b "$CLOUD_IMAGE_NAME"_base.qcow2 \
    hdd.qcow2 "$DISK_SIZE"
}

# Generate an ISO image
generate_seed_iso(){
  cloud-localds seed.img user-data
}

# Boot exisiting cloud-init backed VM
boot_ubuntu_cloud_vm(){
  tmux new-session -d -s "${VM_NAME}_session"
  tmux send-keys -t "${VM_NAME}_session" "sudo qemu-system-x86_64  \
    -machine accel=kvm,type=q35 \
    -cpu host \
    -smp "$PHYSICAL_CORES" \
    -m "$MEMORY" \
    -nographic \
    -device virtio-net-pci,netdev=net0 \
    -netdev user,id=net0,hostfwd=tcp::"$VM_SSH_PORT"-:"$HOST_SSH_PORT" \
    -drive if=virtio,format=qcow2,file="$CLOUD_IMAGE_NAME"-new.img \
    -vnc :0 \
    $@" ENTER
}

# start the cloud-init backed VM
create_ubuntu_cloud_vm(){
  tmux new-session -d -s "${VM_NAME}_session"
  tmux send-keys -t "${VM_NAME}_session" "sudo qemu-system-x86_64  \
    -machine accel=kvm,type=q35 \
    -cpu host \
    -smp "$PHYSICAL_CORES" \
    -m "$MEMORY" \
    -nographic \
    -device virtio-net-pci,netdev=net0 \
    -netdev user,id=net0,hostfwd=tcp::"$VM_SSH_PORT"-:"$HOST_SSH_PORT" \
    -drive if=virtio,format=qcow2,file="$CLOUD_IMAGE_NAME"-new.img \
    -drive if=virtio,format=raw,file=seed.img \
    -vnc :0 \
    $@" ENTER
}

# luanch the VM to install from ISO to Disk
create_vm_from_iso(){
  sudo qemu-system-x86_64 -enable-kvm \
          -cpu host,nx \
          -smp 2 \
          -drive file="$CLOUD_IMAGE_NAME"_base.img,if=virtio \
          -net nic -net user,hostfwd=::"$VM_SSH_PORT"-:"$HOST_SSH_PORT" \
          -m "$MEMORY" \
          -vga "$VGA" \
          -monitor stdio \
          -vnc :0 \
          $@
}

attach_to_vm_tmux(){
  export_metatdata
  tmux attach-session -t "${VM_NAME}_session"
}

ssh_to_vm(){
  export_metatdata
  ssh-keygen -f "/home/${USER}/.ssh/known_hosts" -R "[${HOST_ADDRESS}]:${VM_SSH_PORT}"
  ssh -o "StrictHostKeyChecking no" \
    -i "$VM_NAME"/"$VM_USER" \
    -p "$VM_SSH_PORT" "$VM_USER"@"$HOST_ADDRESS"
}

add_vm_to_inventory(){
export_metatdata
VM_KEY_FILE=$(find "$(cd ..; pwd)" -name $VM_USER)
VM_KEY=$(cat "$VM_KEY_FILE".pub)

# add the new VM to the ansible inventory
    cat << EOF > ${VM_NAME}/${VM_NAME}-inventory.yaml
webservers:
  hosts:
    ${VM_NAME}:
      ansible_connection: ssh
      ansible_host: ${HOST_ADDRESS}
      ansible_ssh_user: ${VM_USER}
      ansible_ssh_port: ${VM_SSH_PORT}
      ansible_ssh_common_args: "-o StrictHostKeyChecking=no -o ControlMaster=auto -o ControlPath=~/.ssh/ansible-%r@%h:%p"
      ansible_ssh_private_key_file: ${VM_KEY_FILE}

EOF
}

gather_facts(){
# gather facts about client
  export_metatdata
  
  ansible-playbook -i $ANSIBLE_INVENTORY_FILE \
      "playbooks/gather-facts.yaml" \
      -u $VM_USER \
      $VERBOSITY
}

run_full_profile(){
# provision the Host with an ansible profile
  export_metatdata

    for file in /"${DEMO_DIR}"/*.yaml
    do
        export PROFILE_PATH=$file

        echo "running $file ..."
        time ansible-playbook -i $ANSIBLE_INVENTORY_FILE \
            $ANSIBLE_PLAYBOOK \
            -u $VM_USER \
            --extra-vars \
            "profile_path='${PROFILE_PATH}' \
            ssh_key_path='${VM_KEY_FILE}' \
            synced_directory='${SYNCED_DIR}' \
            ansible_user='$VM_USER' \
            squash='${SQUASH}' \
            debug_output='${DEBUG}' \
            $VERBOSITY"

    done
}

run_single_step(){
# run a single step of a profile against the host
export_metatdata

  PROFILE_PATH="/home/max/onboardme/configs/ansible_profiles/basic_desktop/$1.yaml"

    time ansible-playbook -i $ANSIBLE_INVENTORY_FILE \
        $ANSIBLE_PLAYBOOK \
        -u $VM_USER \
        --key-file "$VM_KEY_FILE" \
        --extra-vars \
        "profile_path='${PROFILE_PATH}' \
        ssh_key_path='${VM_KEY_FILE}' \
        synced_directory='${SYNCED_DIR}' \
        ansible_user='$VM_USER' \
        squash='${SQUASH}' \
        debug_output='${DEBUG}' \
        $VERBOSITY"
}

connect_console(){
    ansible-console --become-method sudo \
        --become-user $VM_USER \
        -i $ANSIBLE_INVENTORY_FILE \
        --key-file "$VM_KEY_FILE" \
        -u $ANSIBLE_REMOTE_USER 
}

create(){
  export_metatdata
  create_dir
  download_cloud_image
  expand_cloud_image
  create_ssh_key
  create_user_data
  generate_seed_iso
  create_ubuntu_cloud_vm
  attach_to_vm_tmux
}

boot(){
  export_metatdata
  create_dir
  #download_cloud_image
  #expand_cloud_image
  #create_ssh_key
  #create_user_data
  #generate_seed_iso
  boot_ubuntu_cloud_vm
  attach_to_vm_tmux
}

"$@"
