# vm stuff

## QEMU
```bash
# this is for a windows chonker
alias qemu-magic-create-drive='qemu-img create -f qcow2 win10.img 64G'

alias qemu-magic-create-from-iso='qemu-system-x86_64 -hda win10.img -cdrom Win10_21H2_EnglishInternational_x64.iso -boot d -enable-kvm -cpu host -m 4G -vga std -net nic,model=e1000 -net user'

alias qemu-magic-start='qemu-system-x86_64 -hda win10.img -boot c -enable-kvm -cpu host -m 8G -vga std -net nic,model=e1000 -net user'

alias qemu-magic-snapshot='qemu-img create -f qcow2 -b win10.img win10-working-snapshot.img'
```

## Multipass
*note: multipass ended up giving me problems, so I just kept on truckin with KIND for right now.*

```bash
# launches a vm with 2 vCPU, 32G disk, name of node: k8s-worker-1, Ubuntu Image verion 20.04
multipass launch -c 2 -d 32G -m 2G -n k8s-wkr-1 20.04
multipass launch -c 2 -d 32G -m 2G -n k8s-wkr-2 20.04

# I just don't wanna call it a master
multipass launch -c 2 -d 32G -m 2G -n k8s-manager-1 20.04

# to access a multipass instance if you need to
multipass shell k8s-worker-1
```

# K8s stuff
## KIND - because easy local testing on linux

```bash
# creating a quick small cluster (unnamed, defaults to name: kind)
sudo kind create cluster

# adding newly created KIND kubeconfig
sudo kind get kubeconfig > ~/.kube/kubeconfig
```

## HELM - package manager for k9s

### installing helm
```bash
curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
sudo apt-get install apt-transport-https --yes
echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

### installing nextcloud
```bash
helm repo add nextcloud https://nextcloud.github.io/helm/
helm repo update
```
