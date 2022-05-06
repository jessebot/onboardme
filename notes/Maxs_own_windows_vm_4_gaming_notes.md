# QEMU + KVM GPU IOMMU passthrough with Debian Linux Host and Windows 10 Guest


## Getting the GPU PCI Information

Your GPU that you wish to pass through to the VM will often have other devices in its IOMMU group.
If this is the case, ALL devices in that IOMMU group should be passed through to your VM.
This shouldnt be too much of a problem, as those companion devices will likely be audio or busses that 
are attached to the GPU as well. 
This is only really an issue if your GPU for the Host and the GPU for the Guest are in the same IOMMU Group.
If that's the case, you need a patched kernel[idk how to do it yet] or to put the GPU in a differient PCI-e slot on your motherboard.


This script will gather all the PCI devices and sort them cleanly based on their IOMMU Group:

```zsh

cat << EOF > iommu-finder.sh
#!/bin/bash
# change the 999 if needed
shopt -s nullglob
for d in /sys/kernel/iommu_groups/{0..999}/devices/*; do
    n=${d#*/iommu_groups/*}; n=${n%%/*}
    printf 'IOMMU Group %s ' "$n"
    lspci -nns "${d##*/}"
done;
EOF

chmod +x iommu-finder
```

Example script output

```zsh
...
...
IOMMU Group 0 00:00.0 Host bridge [0600]: Intel Corporation 4th Gen Core Processor DRAM Controller [8086:0c00] (rev 06)
IOMMU Group 1 00:01.0 PCI bridge [0604]: Intel Corporation Xeon E3-1200 v3/4th Gen Core Processor PCI Express x16 Controller [8086:0c01] (rev 06)
IOMMU Group 1 01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GP104 [GeForce GTX 1070 Ti] [10de:1b82] (rev a1)
IOMMU Group 1 01:00.1 Audio device [0403]: NVIDIA Corporation GP104 High Definition Audio Controller [10de:10f0] (rev a1)
IOMMU Group 2 00:02.0 VGA compatible controller [0300]: Intel Corporation Xeon E3-1200 v3/4th Gen Core Processor Integrated Graphics Controller [8086:0412] (rev 06)
IOMMU Group 3 00:03.0 Audio device [0403]: Intel Corporation Xeon E3-1200 v3/4th Gen Core Processor HD Audio Controller [8086:0c0c] (rev 06)
...
...

```

From the above output I found the PCI Bus and Device ID of the NVIDIA GPU and its related devices. 

```yaml
Nvidia:
  - GUEST_GPU: GTX 1070ti
    IOMMU_Group: '1'
  - Name: PCI Bridge
    Bus: '00:01.0'
    DeviceId: '8086:0c01'
  - Name: VGA-compatible-controller
    Bus: '01:00.0'
    DeviceId": '10de:1b82'
  - Name: Audio_Device
    Bus: '01:00.1'
    DeviceId": '10de:10f0'
```

Fortunately, all needed of these devices were already in separate IOMMU groups, or bundeled together in [group 1]


To apply these values im going modify kernel modules via scripts.
that will same effect as a kernel mod line in /etc/defaul/grub like:

```zsh

GRUB_CMDLINE_LINUX_DEFAULT="amd_iommu=on iommu=pt kvm.ignore_msrs=1 vfio-pci.ids=<someID-0>,<someID-1>"

```


Creating /etc/initramfs-tools/scripts/init-top/vfio.sh

```zsh

cat << EOF > /etc/initramfs-tools/scripts/init-top/vfio.sh
#!/bin/sh

# VGA-compatible-controller
PCIbusID0="01:00.0"

# audio-device
PCIbusID1="01:00.1"

PREREQ=""

prereqs()
{
   echo "$PREREQ"
}

case $1 in
prereqs)
   prereqs
   exit 0
   ;;
esac

for dev in 0000:"$PCIbusID0" 0000:"$PCIbusID1"
do 
 echo "vfio-pci" > /sys/bus/pci/devices/$dev/driver_override 
 echo "$dev" > /sys/bus/pci/drivers/vfio-pci/bind 
done

exit 0

EOF

```
Make it executable:

```zsh
chmod +x vfio.sh
```

Setting the kernel module options by creating a replacement config file for: "/etc/initramfs-tools/modules"


Create the file in the local dir

```zsh

cat << EOF > modules
# List of modules that you want to include in your initramfs.
# They will be loaded at boot time in the order below.
#
# Syntax:  module_name [args ...]
#
# You must run update-initramfs(8) to effect this change.
#
# Examples:
#
# raid1
# sd_mod
options kvm ignore_msrs=1
EOF

```

Move it into place and correct the ownership and pemrissions

```
sudo mv /etc/initramfs-tools/modules /etc/initramfs-tools/modules.bak
sudo mv modules /etc/initramfs-tools/
sudo chown root:root /etc/initramfs-tools/modules 
sudo chmod 644 /etc/initramfs-tools/modules 
```


CPU Pinning
 <vcpu placement='static'>14</vcpu>
 <iothreads>1</iothreads>
 <cputune>
    <vcpupin vcpu='0' cpuset='1'/>
    <vcpupin vcpu='1' cpuset='2'/>
    <vcpupin vcpu='2' cpuset='3'/>
    <vcpupin vcpu='3' cpuset='4'/>
    <vcpupin vcpu='4' cpuset='5'/>
    <vcpupin vcpu='5' cpuset='6'/>
    <vcpupin vcpu='6' cpuset='7'/>
    <vcpupin vcpu='7' cpuset='9'/>
    <vcpupin vcpu='8' cpuset='10'/>
    <vcpupin vcpu='9' cpuset='11'/>
    <vcpupin vcpu='10' cpuset='12'/>
    <vcpupin vcpu='11' cpuset='13'/>
    <vcpupin vcpu='12' cpuset='14'/>
    <vcpupin vcpu='13' cpuset='15'/>
    <emulatorpin cpuset='0,8'/>
    <iothreadpin iothread='1' cpuset='0,8'/>
 </cputune>
 
 
# simple launch to get into the gui

Once we can get into the GUI we must update some group policy values to set the proper GPU for use with RDP connections

qemu-system-x86_64 \
    -hda win10.img \
    -boot c \
    -machine type=q35,accel=kvm \
    -cpu host,kvm="off" \
    -smp sockets=1,cores=2,threads=2 \
    -m 8G \
    -vga std
    -serial none \
    -parallel none \
    -device vfio-pci,host=01:00.0,multifunction=on \
    -device vfio-pci,host=01:00.1 \
    -net nic,model=e1000 \
    -net user 


We also need to record the ip address for the vm. 
For this example is "10.0.2.15"

Now we can connect via rdp

# Set up a networking bridge, before RDP will work
Make sure bridge-utils is installed:
`sudo apt install bridge-utils`


edit `/etc/network/interfaces`:

```
auto lo
iface lo inet loopback

auto br0
iface br0 inet static
        address 192.168.50.23
        network 192.168.50.0
        netmask 255.255.255.0
        broadcast 192.168.50.255
        gateway 192.168.50.1
        dns-nameservers 192.168.50.1 1.1.1.1
        bridge_ports eth0
        bridge_stp off
        bridge_fd 0
        bridge_maxwait 0
```

Restart networking? :shrug: maybe reboot if you can't figure that out :shrug:

The XML for the networking in virtual manager:
```xml
<interface type="network">
  <mac address="52:54:00:1b:70:45"/>
  <source network="default"/>
  <model type="e1000e"/>
  <address type="pci" domain="0x0000" bus="0x01" slot="0x00" function="0x0"/>
</interface>
```

What we're gonna change it to:
```xml
<interface type="bridge">
  <mac address="52:54:00:1b:70:45"/>
  <source brdige="br0"/>
</interface>
```


# with vnc

```zsh

sudo apt install qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virtinst libvirt-daemon libosinfo-bin xorg virt-manager virt-viewer

sudo systemctl enable --now libvirtd


/etc/libvirt/qemu.conf:

vnc_listen = "0.0.0.0"
vnc_password = your-password


/etc/libvirt/libvirtd.conf

listen_tcp = 1

service libvirtd restart


export VM_NAME="testvm"
export OS_TYPE="Linux"
export OS_VARIANT="ubuntu22.04"
export DISK_NAME="boot.img"
export DISK_SIZE="20G"
export ISO_FILE="ubuntu-22.04-desktop-amd64.iso"
export MEMORY="2G"
export PHYSICAL_CORES="2"
export VGA="cirrus"

qemu-img create -f qcow2 "$DISK_NAME" "$DISK_SIZE"

sudo qemu-system-x86_64 -enable-kvm \
        -cpu host \
        -cdrom "$ISO_FILE" \
        -drive file="$DISK_NAME",format=qcow2 \
        -m "$MEMORY" \
        -name "$VM_NAME" \
        -vnc localhost:10.0

sudo virt-install --name yourVM \
  --memory 2048 \
  --vcpus 2 \
  --disk size=20 \
  --cdrom /home/user/Downloads/ubuntu-17.10.1-desktop-amd64.iso
  --graphics vnc,listen=0.0.0.0 \
  --noautoconsole

ssh -v -L 5900:127.0.0.1:5900 -N -f 192.168.1.100


```

To get to bios, this worked, and spits you into a shell, which you then hit exit on and select boot manager.
  
sudo qemu-system-x86_64 \
   # primary hard disk \
   -drive id=disk0,if=virtio,cache=none,format=raw,file=Win10-AlternateInstall.img \
   # Windows Installer ISO Image \
   -drive file=Win10_21H2_EnglishInternational_x64.iso,index=1,media=cdrom \
   # Driver installer ISO \
   #-drive file=virtio-win-0.1.141.iso,index=0,media=cdrom \
   -boot c \
   -machine type=q35,accel=kvm \
   -cpu host,kvm="off" \
   -smp sockets=1,cores=2,threads=2 \
   -m 8G \
   -serial none \
   -parallel none \
   # GTX 1070 TI \
   -device vfio-pci,host=01:00.0,multifunction=on \
   # GTX 1070 TI HDMI Audio \
   -device vfio-pci,host=01:00.1 \
   -net nic,model=e1000 \
   -net user \
   -bios /usr/share/qemu/OVMF.fd \
   # if you need a remote connection
   -vnc 127.0.0.1:2


sudo qemu-system-x86_64 \
   -hda Win10-AlternateInstall.img \
   -boot c \
   -machine type=q35,accel=kvm \
   -cpu host,kvm="off" \
   -smp sockets=1,cores=2,threads=2 \
   -m 8G \
   -serial none \
   -parallel none \
   -device vfio-pci,host=01:00.0,multifunction=on \
   -device vfio-pci,host=01:00.1 \
   -device virtio-net,netdev=vmnic \
   -netdev user,id=vmnic \
   -net nic,model=e1000 \
   -net user \
   -bios /usr/share/qemu/OVMF.fd
