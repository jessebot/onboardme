---
layout: default
parent: Android
grand_parent: Operating Systems
title: Screen Mirroring
permalink: /os/android/screen-mirroring
---

## Screen Mirroring from Android device
We'll be using [scrcpy](https://github.com/Genymobile/scrcpy) in this guide, which bundles abd, so you don't need to install abd in addition to this.

### Installation and Setup On Debian
Do _NOT_ use the apt package. It is incredibly out of date. Use the snap package.
```bash
sudo snap install scrcpy
```
*NOTE*: Make use `/snap/bin` is in your path

Make sure your phone is also in debug mode:

```bash
# alias already present in onboardme.py .bashrc
alias adb='scrcpy.adb'

# Start the server with scrcpy's bundled adb
adb start-server
```

### Put your phone in Debug mode and connect via USB
#### Step One
Settings > About Phone > Software information > Scroll down to ‘Build number’ and tap that box 7 times. If debug mode was already activated previously, you will receive a message that says ‘No need, developer mode has already been enabled’.

#### Step Two
Settings > Search > Type ‘developer options’ > Select the ‘Developer options’ under ‘Developer options’ (and not the one under ‘Screen reader’) > Scroll down to ‘USB debugging’ directly under the ‘Debugging header’ and slide the switch from Off (left) to On (right) > Press ‘OK’ to confirm you want to enable USB debugging.

Then connect your phone via USB and you will get a message on your phone that says "Allow USB debugging?". Tap Allow. Finally, you'll get a "Allow access to phone data?" and you should tap allow for that too.

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
scrcpy
```
:party:

# Troubleshooting
Is the device not showing up? Try disconnecting your phone and unmounting it via the file explorer.
Then restart the server with:
```bash
adb kill-server
adb start-server
```

Then try connecting again and it _should_ work, but you may need to remove all allowed developer USB connections and restart the phone before trying. That's all I got.
