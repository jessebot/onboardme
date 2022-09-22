---
layout: default
title: WSL
grand_parent: Operating Systems
parent: Windows
permalink: /os/windows/wsl
---

# WSL (Windows Subsystem for Linux)
These instructions should install WSL 2, but on some older versions of Windows, it will install WSL 1, but that is addressed in the final section of this doc.

Should be able to get to this by first hitting 🪟 Key, and then typing "devleoper settings" and hitting `enter`. 
(Equivelent of: Settings > Update and Security > For developers)

Toggle "Developer Mode" to `on`.

Run this in powershell:
```powershell
wsl --install
```

After the install, go to 🪟 key > turn windows features on or off (it's in control panel).

Then you should be able to scroll down to Windows Subsystem for Linux and check the box before saving and quitting.

FINALLY, you can bring up 🪟 key > microsoft store > Debian (app) and hit install.

---
## Disable terminal bell/beep in wsl

For BASH:
```bash
sudo sed -i 's/# set bell-style none/set bell-style none/' /etc/inputrc
```

For VIM:
```vim
set visualbell
set t_vb=
```
Requires restart of WSL app (in my case, Debian).

---
## VPN causing issues with DNS resolution
Edit `/etc/wsl.conf` and uncomment `generateNetworkConf=false` or whatever it's called, and set it to `false` if it isn't already. Then unlink your `etc/resolv.conf` and modify it to be the VPN's name servers only.

---
## Can't echo `brew` path into `.bashrc`

When you try this:

```bash
echo "export PATH=$PATH:/home/linuxbrew/.linuxbrew/bin" >> ~/.bashrc
```

You will get some errors about characters like this `(`. It's because by default, windows puts their own awful spaced and parenthesed directories into your default path, and BASH is expanding the `$PATH` variable on the commandline, without escaping any of that nonsense.

Just open up vim and manually put in the following to it's own line in your `.bashrc`:

```bash
export PATH=$PATH:/home/linuxbrew/.linuxbrew/bin
```

---
## Installing Docker for wsl
You'll need to first install [Docker Desktop for Windows](https://docs.docker.com/desktop/windows/install/).

You'll need your Linux distro to be using wsl 2, and you can check with this in powershell:
```powershell
PS C:\Users\jesse> wsl -l -v
  NAME      STATE           VERSION
* Debian    Stopped         2
```

In the above example I am already running my distro, Debian on the wsl 2 backend, but if you're not, you can fix it like this (replacing Debian with your distro).
```powershell
wsl.exe --set-version Debian 2
```

To set v2 as the default version for future installations, run:
```powershell
wsl.exe --set-default-version 2
```

After all of that, which takes easily 15 minutes, you'll need to reboot, and then you can launch Docker from windows, and then go to:
⚙️ Settings > Resources > WSL

Toggle the switch to `on` for your distro. Fin.

More info on Docker Desktop WSL 2 backend and Docker is available [here](https://docs.docker.com/desktop/windows/wsl/).

---
## Launching Windows File Explorer for `pwd` in Linux
From WSL, you'll want to run the following command, and that will launch File Explorer on Windows for your current Linux directory.

```bash
explorer.exe .
```

I know it's confusing to see exe run from a Linux shell, but bear with me. In my case, this launched file explorer to my home dir, which was located here in windows:
```powershell
\\wsl$\Debian\home\jesse
```
Which, in the URI bar, will show as 📂 > Network > wsl$ > Debian > home > jesse
