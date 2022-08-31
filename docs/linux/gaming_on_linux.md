---
layout: default
title: gaming
parent: Linux
nav_order: 2
---

# Gaming on Linux

## Wine
If you're on Debian, you want the instructions on [winehq.com](https://wiki.winehq.org/Debian) which are basically:


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

## Xbox controller for Debian drivers
https://launchpad.net/~grumbel/+archive/ubuntu/ppa

## Misc
ROMS megathread: [https://r-roms.github.io/](https://r-roms.github.io/)

Also, in my travels I found these:
- [PlayOnLinux](https://www.playonlinux.com/)
- [u/Snoo-78612's guide to VivaPinata on Reddit](https://www.reddit.com/r/VivaPinata/comments/jke4er/viva_pinata_gnulinux_installation_guide/)
