# Random Notes

## Gaming on Linux

If you're on Debian, you want the instruction on [winehq.com](https://wiki.winehq.org/Debian) which are basically:

```bash
# Enable 32 bit packages (if you haven't already): 
sudo dpkg --add-architecture i386

# Download and install the repository key: 
wget -nc https://dl.winehq.org/wine-builds/winehq.key
sudo apt-key add winehq.key

# create a *.list under /etc/apt/sources.list.d/ with the following content in this case for Debian bullseye
echo "deb https://dl.winehq.org/wine-builds/debian/ bullseye main" > /etc/apt/sources.list.d/wine.list

# update packages
sudo apt update
```

Then, and ONLY THEN can you run: `sudo apt install winehq-staging`

## apt notes

Thanks to Vaibhav for their solution [here](https://vskulkarni.wordpress.com/2011/10/07/gpg-error-httpppa-launchpad-net/) for when you get this error:
```bash
W: GPG error: http://ppa.launchpad.net lucid Release: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 4DEF31B9A9E345C0
```

It's *THIS* command: 

```bash
# 4DEF31B9A9E345C0 is your KEYID from the above error
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 4DEF31B9A9E345C0
```

- [How does the vim write with sudo trick work?](https://stackoverflow.com/questions/2600783/how-does-the-vim-write-with-sudo-trick-work)
- Pretty view markdown: `pandoc README.md | lynx -stdin`

## Firewall notes
- [How to control internet access for each program?](https://askubuntu.com/questions/45072/how-to-control-internet-access-for-each-program)

## UFW notes
Need to get `$remote_ip` at time of running if this is being set up as a secondary machine
```bash
ufw allow from $remote_ip to any port 22
```

This is to create special firewall configs for annoying apps want to phone home while they're supposed to be not running:
```bash
ufw app list
# move special app 
cp ufw/* /etc/ufw/applications.d
ufw app update discord
ufw app info discord
ufw deny discord
```

## K8s stuff

### KIND - because easy local testing on linux

```bash
# creating a quick small cluster (unnamed, defaults to name: kind)
sudo kind create cluster

# adding newly created KIND kubeconfig
sudo kind get kubeconfig > ~/.kube/kubeconfig
```

### vm stuff
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
