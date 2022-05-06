#!/bin/bash
############
# Script to launch qemu-kvm guest VMs on a headless remote host
# This script utilizes qemu-system-x86_64 to create the VM instead of
# using virt-manager to prevent the need to create XML config files
# as well as to be able to manage the VMs without a UI/GUI
#
# This bash script is a proof-of-concept that ports the previous 
# VMM work found here: https://www.cloudydev.net/dev_ops/multipass/
# from multipass to QEMU/KVM
#
# The need to remove multipass derives from the fact that multipas 
# does not easliy work with non-ubuntu images, nor will it work to
# test .iso live usb images, which I need.
# 
# Multipass also cannot provide hardware accelerated (GPU) windows
# guest VMs, which I also need.
#
# TODO:
#  
# This script should be ported to python and then made into
# an ansible role.
#
# SSH-keys should be stored in a keyvault
#
# vm-metadata should be loaded from file/database
#
# Host Machine Apt packages:
# grub-pc-bin nmap net-tools cloud-image-utils whois
# qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virtinst libvirt-daemon libosinfo-bin xorg virt-manager virt-viewer


# VM metadata
export HOST_ADDRESS="192.168.50.100"
export HOST_SSH_PORT="22"
export VM_NAME="testvm"
export VM_USER="vmadmin"
export VM_SSH_PORT="1234"
export DISK_NAME="boot.img"
export DISK_SIZE="20G"
export ISO_FILE="ubuntu-22.04-live-server-amd64.iso"
export UBUNTU_CODENAME="jammy"
export CLOUD_IMAGE_NAME="${UBUNTU_CODENAME}-server-cloudimg-amd64"
export CLOUD_IMAGE_URL="https://cloud-images.ubuntu.com/jammy/current"
export MEMORY="4G"
export PHYSICAL_CORES="2"
export VGA="std"
export VM_KEY=""
export VM_KEY_FILE="$VM_USER"

# create a directory to hold the VM assets
# this is gross, it'll be fixed in the python script
mkdir "$VM_NAME"
cd "$VM_NAME"

# download a cloud image as .img
# this should accomodate a file-type flag to
# allow downloading other image types
wget -c -O "$CLOUD_IMAGE_NAME".img \
  "$CLOUD_IMAGE_URL"/"$CLOUD_IMAGE_NAME".img

# these two functions will be needed for creating the 
# overlay filesystem, WIP
#
# convert the .img to qcow2 to use as base layer
#qemu-img convert -f raw \
#  -O qcow2 "$CLOUD_IMAGE_NAME"_original.img \
#  "$CLOUD_IMAGE_NAME".qcow2
#
# create the next layer on the image
#qemu-img create -f qcow2 \
#  -F qcow2 \
#  -o backing_file="$CLOUD_IMAGE_NAME"_base.qcow2 \
#  "$VM_NAME".qcow2

# create a ssh key for the user and save as a file w/ prompt
# wildly insecure, do not use in prod, needs to use a keyvault
ssh-keygen -C "$VM_USER" \
  -f "$VM_KEY_FILE" \
  -N '' \
  -t rsa

VM_KEY_FILE=$(find "$(cd ..; pwd)" -name $VM_USER)
VM_KEY=$(cat "$VM_KEY_FILE".pub)

# should be a template file
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

# create a disk
#qemu-img create -f qcow2 -F qcow2 -b "$CLOUD_IMAGE_NAME"_base.qcow2 hdd.qcow2 "$DISK_SIZE"

# Generate an ISO image
cloud-localds seed.img user-data

# start the VM
tmux new-session -d -s "${VM_NAME}_session"
tmux send-keys -t "${VM_NAME}_session" "sudo qemu-system-x86_64  \
  -machine accel=kvm,type=q35 \
  -cpu host \
  -smp "$PHYSICAL_CORES" \
  -m "$MEMORY" \
  -nographic \
  -device virtio-net-pci,netdev=net0 \
  -netdev user,id=net0,hostfwd=tcp::"$VM_SSH_PORT"-:"$HOST_SSH_PORT" \
  -drive if=virtio,format=qcow2,file="$CLOUD_IMAGE_NAME".img \
  -drive if=virtio,format=raw,file=seed.img \
  -vnc :0 \
  $@" ENTER

tmux attach-session -t "${VM_NAME}_session"

#ssh -o "StrictHostKeyChecking no" \
#  -i testvm/"{VM_USER}" -vvvv \
#  -p "$VM_SSH_PORT" "$VM_USER"@"$HOST_ADDRESS"

#ssh -i "$VM_KEY_FILE" \
#  -p 2222 "$VM_USER"@localhost

# TODO 
# create an iso image https://quantum-integration.org/posts/install-cloud-guest-with-virt-install-and-cloud-init-configuration.html
#qemu-img create -f qcow2 -o \
#    backing_file=./master/centos-7-cloud.qcow2 \
#    example.qcow2

# luanch the VM to install from ISO to Disk
#sudo qemu-system-x86_64 -enable-kvm \
#        -cpu host,nx \
#        -smp 2 \
#        -drive file="$CLOUD_IMAGE_NAME"_base.img,if=virtio \
#        -net nic -net user,hostfwd=::"$VM_SSH_PORT"-:"$HOST_SSH_PORT" \
#        -m "$MEMORY" \
#        -vga "$VGA" \
#        -monitor stdio \
#        -vnc :0 \
#        $@
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