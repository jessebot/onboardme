---
layout: default
title: Gaming
permalink: /gaming
desciption: "Everything to do with gaming on Debian Bookworm."
---

# State of Gaming On Debian Bookworm
This is a guide for gaming on Debian Bookworm. Below we mention several closed source applications and proprietary hardware. We are not affiliated with any of these applications or hardware companies and do not recieve any compensation for preparing this guide. This guide is just what worked for us and mentions the apps and hardware that we found the most success with.

This page was last updated on (2023-01-29 10:56:52.0 +0100).

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

Then reboot again, and make sure again, that everything is connected. Steam VR should prompt you for your password and then guide you through the room setup. Remember, flatpak will not prompt for your password to sudo install anything, and so it may not work for VR, so we currently recommend you use apt, not flatpak, for installing steam on Debian Bookworm (last update: 2023-01-29 10:57:12.0 +0100).

### Audio Troubleshooting for Vive VR Headsets
We recommend you install `pavucontrol`, which is a GUI for pulseaudio.

```bash
sudo apt install pavucontrol
```

This will allow you to disable an audio device. If you're having trouble with Vive Pro Headsets, there are many suggestions online, but personally, we chose to just use a third party set of wireless earbuds, as the sound is far more consistent.

To use a different audio source, here's how to do it with pavucontrol:

```bash
# type this in the terminal and hit enter, it will launch the GUI
pavucontrol
```

In the GUI at the top right side, click the "Configuration" tab and set all audio devices you don't want to use to "Off". This should include a device listed as "VIVE Pro Mutimedia Audio":

<a href="https://raw.githubusercontent.com/jessebot/onboardme/9b61d4a07ba2d99514dff1c368a804c92c9ea83e/docs/onboardme/screenshots/pavucontrol_vive_audio.png">
  <img src="https://raw.githubusercontent.com/jessebot/onboardme/9b61d4a07ba2d99514dff1c368a804c92c9ea83e/docs/onboardme/screenshots/pavucontrol_vive_audio.png" width="600">
</a>

In our case, since we have a living room VR headset, we mirror the VR view to a projector, and then we use a bluetooth audio hub connected via an aux cable to our living room PC's headphone jack. Connected to the bluetooth audio hub are a set of small speakers as well as the aforementioned wireless earbuds, which is why in the above screenshot you see "Built in Audio".

We are not affiliated with any of these brands below and do not recieve any money for advertising them. These are all just the best mid-tier price and quality devices that suit our needs and seem to work with Debian:

- [Avantree Orbit - Bluetooth 5 Audio Hub](https://avantree.com/eu/orbit-tc580-bluetooth-transmitter-for-tv)

These are connected to the bluetooth hub:
- [JLAB Epic Air Sport ANC True Wireless Earbuds - mid-tier wireless earbuds](https://www.jlab.com/products/epic-air-sport-anc-true-wireless-earbuds)
- [Mackie CR3 Duo Pack - Okay studio monitors with bluetooth capability](https://www.coolblue.be/en/product/741786/mackie-cr3-duo-pack.html)

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
