#!/bin/bash
############
# Script to launch qemu-kvm guest VMs on a headless remote host
# Vleermuis 2022

# Depends on grub-pc-bin, nmap, net-tools, cloud-image-utils, whois

# VM metadata
export_metatdata(){
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
}

# create a directory to hold the VM assets
create_dir(){
  mkdir "$VM_NAME"
  cd "$VM_NAME"
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

create_user_data(){
cat > user-data <<EOF
#cloud-config
#vim:syntax=yaml

cloud_config_modules:
 - runcmd

cloud_final_modules:
 - [users-groups, always]
 - [scripts-user, once-per-instance]

users:
  - name: ${VM_USER}
    groups: [ wheel ]
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

# start the VM
start_ubuntu_cloud_vm(){
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

attach_to_vm_tmux(){
  export_metatdata
  tmux attach-session -t "${VM_NAME}_session"
}

ssh_to_vm(){
  export_metatdata
  ssh-keygen -f "/home/${USER}/.ssh/known_hosts" -R "[${HOST_ADDRESS}]:${VM_SSH_PORT}"
  ssh -o "StrictHostKeyChecking no" \
    -i testvm/"$VM_USER" \
    -p "$VM_SSH_PORT" "$VM_USER"@"$HOST_ADDRESS"
}


# TODO 
# create an iso image https://quantum-integration.org/posts/install-cloud-guest-with-virt-install-and-cloud-init-configuration.html
#qemu-img create -f qcow2 -o \
#    backing_file=./master/centos-7-cloud.qcow2 \
#    example.qcow2

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

main(){
  export_metatdata
  create_dir
  download_cloud_image
  expand_cloud_image
  create_ssh_key
  create_user_data
  generate_seed_iso
  start_ubuntu_cloud_vm
}

"$@"

#
#
#  Connecting to the VM after install is done
#  1. SSH from the Host to Guest
#   ssh -X -Y -p "$VM_SSH_PORT" localhost
#
#  2. SSH from remote client to host and be redirected to guest
#   ssh -X -Y -p "$VM_SSH_PORT" max@"$HOST_ADDRESS"
#
#  3. Connect to Guest using QEMU's VNC server
#   "$HOST_ADDRESS":"$VM_SSH_PORT"
#  Get status of port
#
#  nmap -p 1234 localhost
#
#  VNC tunnel https://gist.github.com/chriszarate/bc34b7378d309f6c3af5
#
#
#  ssh -o "StrictHostKeyChecking no" \
#    -N -L 5001:"$HOST_ADDRESS":5900 \
#    -p "$VM_SSH_PORT" "VM_USER"@"HOST_ADDRESS"