---
layout: default
title: QEMU
parent: Virtual Machines
permalink: /docs/vm/qemu
---

## QEMU
```bash
# this is for a windows chonker
alias qemu-magic-create-drive='qemu-img create -f qcow2 win10.img 64G'

alias qemu-magic-create-from-iso='qemu-system-x86_64 -hda win10.img -cdrom Win10_21H2_EnglishInternational_x64.iso -boot d -enable-kvm -cpu host -m 4G -vga std -net nic,model=e1000 -net user'

alias qemu-magic-start='qemu-system-x86_64 -hda win10.img -boot c -enable-kvm -cpu host -m 8G -vga std -net nic,model=e1000 -net user'

alias qemu-magic-snapshot='qemu-img create -f qcow2 -b win10.img win10-working-snapshot.img'
```
