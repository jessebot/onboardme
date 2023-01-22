---
layout: default
title: Gaming
permalink: /gaming
desciption: "Everything to do with gaming on Debian Bookworm."
---

# State of Gaming On Debian Bookworm
This page was last updated on (2023-01-22 19:21:26.0 +0100).

## Steam on Debian - via apt - (Recommended For VR on Debian Bookworm)

First: If you have steam installed any other way, uninstall it as well as purge your nvidia drivers.

Then start by updating your apt sources. Use the editor of your choice. I use vim below:

```bash
# update your sources to include non-free stuff
sudo vim /etc/apt/sources.list
```

Then add the following lines if they don't already exist:

```bash
deb http://deb.debian.org/debian/ bookworm main contrib non-free
deb http://deb.debian.org/debian/ bullseye main contrib non-free
```

**NOTE: you need both the bookworm and bullseye lines because without it, you cannot find the `steam:i386` package in the future parts of this tutorial.**


Now update to pull the latest sources and then upgrade, for good measure:

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

That should update your xorg.conf, but you'll also need to modify it anyway, and add the following line to your nvidia "Device" section:

```bash
Option "AllowHMD" "yes"
```

Example of our "Device" secion in our `/etc/X11/xorg.conf`:

```
Section "Device"
    Identifier     "Device0"
    Driver         "nvidia"
    VendorName     "NVIDIA Corporation"
    Option         "AllowHMD" "yes"
EndSection
```

You don't need to reboot again, but like, who knows, we did :shrug:

Now, if you're trying to do stuff with VR, you need to make sure your headset is plugged into the GPU and ON!

Then you can list your devices, that hopefully shows your headset with:

```bash
nvidia-xconfig --query-gpu-info
xrandr --verbose
```

Launch steam from the terminal by using the command: `steam`.

Now, if you're trying to use a VR headset, you can install "Steam VR" from the steam steam store. You will need to connect your VR headset, any base stations you have, and of course, your controllers, and then Steam VR SHOULD work, but for good measure, we also installed the following:

```bash
sudo apt install libva-x11-2:i386 libva2:i386 libgdk-pixbuf2.0-0:i386 libxtst6:i386 libgtk2.0-0:i386 libbz2-1.0:i386 libvdpau1:i386
```

Then reboot again, and make sure again, that everything is connected. Steam VR should prompt you for your password and then guide you through the room setup. Remember, flatpak will not prompt for your password to sudo install anything, and so it may not work for VR, so we currently recommend you use apt, not flatpak, for installing steam on Debian Bookworm (last update: 22-01-2023).


## Xbox controller drivers
Debian says [most controllers *should* "just work"](https://wiki.debian.org/Gamepad) now.
Still probably install the `steam-devices` package from apt though.


## Steam on Debian - via flatpak
(NOTE: getting steam VR to work via flatpak is pain, and we don't recommend it)

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



## Misc Useful
ROMS megathread: [https://r-roms.github.io/](https://r-roms.github.io/)

Also, in my travels I found these:
- [PlayOnLinux](https://www.playonlinux.com/)
- [u/Snoo-78612's guide to VivaPinata on Reddit](https://www.reddit.com/r/VivaPinata/comments/jke4er/viva_pinata_gnulinux_installation_guide/)

[Lutris]:
