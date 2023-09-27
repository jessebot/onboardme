---
layout: default
parent: Android
grand_parent: Operating Systems
title: Screen Mirroring
permalink: /os/android/screen-mirroring
---


# Screen Mirroring from Android device

We'll be using [scrcpy](https://github.com/Genymobile/scrcpy) in this guide.

## Installation

<details>
  <summary>`scrcpy` via `brew` and `apt` on Debian</summary>

  First install adb with apt:

  ```bash
  # use apt to install adb which scrcpy needs
  sudo apt install -y adb
  ```

  Then install [scrcpy](https://github.com/Genymobile/scrcpy) with brew:

  ```bash
  # use linuxbrew to install scrcpy
  brew install scrcpy

  # add scrcpy to your path if you haven't already
  export PATH="$PATH:/home/linuxbrew/.linuxbrew/bin"
  ```

</details>


<details>
  <summary>Install via `snap` on Debian</summary>

  I don't use the snap store anymore, but if you do, the below guide _may_ be of use (but is no longer tested!)

  The snapstore verson of `scrcpy` installs `adb` for you, so you don't need to install it.

  Do _NOT_ use the apt package. It is incredibly out of date. Use the snap package.
  ```bash
  sudo snap install scrcpy
  ```
  *NOTE*: Make use `/snap/bin` is in your path
  
  Make sure your phone is also in debug mode:
  
  ```bash
  alias adb='scrcpy.adb'
  ```

</details>


## Start the server with adb

```bash
adb start-server
```

### Put your phone in Debug mode and connect via USB
#### Step One
Settings > About Phone > Software information > Scroll down to ‘Build number’ and tap that box 7 times. If debug mode was already activated previously, you will receive a message that says ‘No need, developer mode has already been enabled’.

#### Step Two
Settings > Search > Type ‘developer options’ > Select the ‘Developer options’ under ‘Developer options’ (and not the one under ‘Screen reader’) > Scroll down to ‘USB debugging’ directly under the ‘Debugging header’ and slide the switch from Off (left) to On (right) > Press ‘OK’ to confirm you want to enable USB debugging.

Then connect your phone via USB and you will get a message on your phone that says "Allow USB debugging?". Tap Allow. Finally, you'll get a "Allow access to phone data?" and you should tap allow for that too.

After that, if it still doesn't work, you may need to plug the USB kabel from your computer into your phone, and then on your phone, pull down the top menu that's normally for notificiations, and select "USB for ..." and update the setting to USB for file transfer.

And if that doesn't work, try using a different kabel, and remove any kabel extenders from the equation. It could be that your phone only works in USB debug mode with branded kabels. This is the case with the Samsung Galaxy S22 Ultra 5G, for instance.

#### Step Three
List devices and verify their integrity.
```bash
# should list a device if your phone is plugged in and working
adb devices

# this will put you into a shell ot verify everything is working correctly
adb shell
```

In the adb shell, try this:
```bash
# check how many processors you have
cat /proc/cpuinfo | grep -E 'processor|BogoMIPS'

# exit the shell when done.
exit
```

### Connect to your phone via WIFI
Restart the connection on a new port (port number is arbitrary)
```bash
adb tcpip 2233
```
You should get this: `restarting in TCP mode port: 2233`

Now you need to get your phone's local IP address. You can check your phone, pihole, or router settings for this. Under pihole or the router, you are probably connected via DHCP, so try there. Once you have the IP address you can do this:

```bash
# assuming your phone's IP is 192.168.42.42 and you selected port 2233 above
adb connect 192.168.42.42:2233
```
That should return: `connected to 192.168.42.42:2233` You can verify for sure with this:
```bash
adb devices
```
Which should return `List of devices attached` followed by something like `192.168.42.42:2233 device`

FINALLY, you can now run this to get your phone mirrored:
```bash
scrcpy --select-tcpip
```

and if that fails, you can either upgrade your graphics card drivers, or try this command:

```bash
scrcpy --render-driver=software --select-tcpip
```

:tada:

# Troubleshooting


## device not showing up in adb?

Try disconnecting your phone and unmounting it via the file explorer. Then restart the server with:

```bash
adb kill-server
adb start-server
```

Then try connecting again and it _should_ work, but you may need to remove all allowed developer USB connections and restart the phone before trying. That's all I got.

## `Error: Could not create renderer`

If you're getting this error:

```console
$ scrcpy --select-tcpip
scrcpy 2.1.1 <https://github.com/Genymobile/scrcpy>
INFO: ADB device found:
INFO:     --> (tcpip)  192.168.50.180:2233             device  SM_G998B
/home/linuxbrew/.linuxbrew/Cellar/scrcpy/2.1.1/share/scrcpy/scrcpy-server: 1 file pushed, 0 skipped. 1.5 MB/s (56995 bytes in 0.036s)
[server] INFO: Device: [samsung] samsung SM-G998B (Android 13)
ERROR: Could not create renderer: Couldn't find matching render driver
WARN: Killing the server...
```

This is probably due to your graphics card drivers, and according to [this issue comment](https://github.com/Genymobile/scrcpy/issues/58#issuecomment-747511886) you can solve this by running:

```bash
scrcpy --render-driver=software --select-tcpip
```
