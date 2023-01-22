---
layout: default
title: Gaming
permalink: /gaming
desciption: "Everything to do with gaming on Debian Bookworm."
---

# State of Gaming On Debian Bookworm
This page was last updated on (2023-01-14 19:01:13.0 +0100).

## Lutris
On Debian, install [Lutris] via flatpak:

```bash
# installing lutris
flatpak install net.lutris.Lutris

# running lutris
flatpak run net.lutris.Lutris

# launch lutris through flatpak; this can also go in your .bashrc
alias lutris="flatpak run net.lutris.Lutris"
```

The version of lutris in apt had issues, and we didn't try snap.

## Playing an Epic Games Store game
This has been so difficult to do with my graphics card via lutris, that I
actually rebought a game I originally bought via Epic Games, on steam instead.

But if the game you're trying to play isn't vram intense, here's the process anyway:

1. Install ESO (the Epic Games Store) via lutris.
On debian, this has to be from flatpak installed lutris.

<img src="" width="800">

Then you'll be guided through installing everything you need.

2. On the left side menu for lutris, select Games. Select Epic Games Store.

3. Select the game you want to play and install it from ESO.

4. Launch the game from Epic Games Store. Don't launch the game from lutris directly!

### Saves
Saves will default go into:

```
# in this dir you'd have a gaming studio named dir, and in there, the games you own by them
~/Games/epic-games-store/dosdevices/c:/users/$(whoami)/Saved\ Games/
```

## Steam on Debian - via apt - For VR

First: If you have steam installed any other way, uninstall it as well as purge your nvidia drivers.

Then start by updating your apt sources. Use the editor of your choice. I use vim below:

```bash
# update your sources to include non-free stuff
sudo vim /etc/apt/sources.list
```

Then add the following line if it does not already exist:

```bash
deb http://deb.debian.org/debian/ bookworm main contrib non-free
deb http://deb.debian.org/debian/ bullseye main contrib non-free
```

**NOTE: you need both the bookworm and bullseye lines because without it, you cannot find `steam:i386` in the future parts of this tutorial.**


Now update to get the latest stuff:

```bash
sudo apt update
sudo apt upgrade
```

Now you can install steam, steam-devices, and nvidia drivers:

```bash
sudo apt install steam:i386 steam-devices
sudo apt install nvidia-driver firmware-misc-nonfree nvidia-xconfig

# if this doesn't work, try a reboot :shrug:
sudo nvidia-xconfig
```

YOU MUST NOW REBOOT. Then you can do:

```bash
sudo nvidia-xconfig
```

Now, if you're trying to do stuff with VR, you need to make sure your headset is plugged into the GPU and ON!

Then you can list your devices, that hopefully shows your headset with:

```bash
nvidia-xconfig --query-gpu-info
xrandr --verbose
```


## Steam on Debian - via flatpak
Install Steam via flatpak:

```bash
# install steam
flatpak install com.valvesoftware.Steam

# run steam
flatpak run com.valvesoftware.Steam
```

Steam via snap on Debian had font issues. Steam on apt instructions are above.

Saves default go into:

```bash
# 1262340 is just the number I have locally, but the directory will have a different number for you
~/.var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps/compatdata/1262340/pfx/drive_c/users/steamuser/Saved\ Games
```

## Wine
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

# update packages first
sudo apt update

sudo apt install winehq-staging
```

## Xbox controller drivers
Debian says [most controllers *should* "just work"](https://wiki.debian.org/Gamepad) now.
Still probably install the `steam-devices` package from apt though.


## Misc Useful
ROMS megathread: [https://r-roms.github.io/](https://r-roms.github.io/)

Also, in my travels I found these:
- [PlayOnLinux](https://www.playonlinux.com/)
- [u/Snoo-78612's guide to VivaPinata on Reddit](https://www.reddit.com/r/VivaPinata/comments/jke4er/viva_pinata_gnulinux_installation_guide/)

[Lutris]:
