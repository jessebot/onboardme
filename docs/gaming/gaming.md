---
layout: default
title: Gaming
permalink: /gaming
desciption: "Everything to do with gaming on Linux or MacOS"
---

# Gaming Where You Weren't Meant To
Everything we know about gaming on Debian (tested on Bookworm).

## Lutris
On Debian, install lutris via flatpak:

```bash
# installing lutris
flatpak install net.lutris.Lutris

# running lutris
flatpak run net.lutris.Lutris
```

The version of lutris in apt had issues.

## Playing an Epic Games Store game
1. Install ESO (the Epic Games Store) via lutris.
On debian, this has to be from flatpak installed lutris.

<img src="" width="800">

Then you'll be guided through installing everything you need.

2. On the left side menu for lutris, select Games. Select Epic Games Store.

3. Select the game you want to play and install it from ESO.

4. Launch the game from Epic Games Store. Don't launch the game from lutris directly!

### Xbox controller for Debian drivers
Debian says [most controllers *should* "just work"](https://wiki.debian.org/Gamepad) now.
Still probably install the `steam-devices` package from apt though.

We previously used [this](https://launchpad.net/~grumbel/+archive/ubuntu/ppa),
but it's a bit out of date now, given that `apt-key` is deprecated.
Will update this later with better instructions, if any.

## Steam on Debian
Install Steam via flatpak:

```bash
# install steam
flatpak install com.valvesoftware.Steam

# run steam
flatpak run com.valvesoftware.Steam
```

Steam via snap on Debian had font issues. Steam on apt didn't work at all.

### Wine
If you're on Debian, and you really have to install wine directly, you want the
instructions on [winehq.com](https://wiki.winehq.org/Debian) which are basically:

```bash
# Enable 32 bit packages (if you haven't already):
sudo dpkg --add-architecture i386

# Download and install the repository key:
wget -nc https://dl.winehq.org/wine-builds/winehq.key
sudo apt-key add winehq.key

# create a *.list under /etc/apt/sources.list.d/ with the following content in this case for Debian bullseye
sudo echo "deb https://dl.winehq.org/wine-builds/debian/ bullseye main" > /etc/apt/sources.list.d/wine.list

# update packages
sudo apt update

#Then, and ONLY THEN can you run
sudo apt install winehq-staging
```

## Misc
ROMS megathread: [https://r-roms.github.io/](https://r-roms.github.io/)

Also, in my travels I found these:
- [PlayOnLinux](https://www.playonlinux.com/)
- [u/Snoo-78612's guide to VivaPinata on Reddit](https://www.reddit.com/r/VivaPinata/comments/jke4er/viva_pinata_gnulinux_installation_guide/)
