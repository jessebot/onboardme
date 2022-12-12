---
layout: default
title: RDP
parent: Screen Sharing
permalink: /screen-sharing/rdp
description: "Everything we know about RDP"
---

# RDP

## RDP from macOS to Debian based distros

Make sure the remote ssh server supports X11. Make sure these lines are in your `/etc/ssh/sshd_config` file:

```sshconfig
X11Forwarding yes
X11UseLocalhost yes
```

Install an X11 server and an RDP client on your mac with:

```bash
brew install --cask xquartz
brew install freerdp
```

*Then you should reboot 🤷*

Xquartz provides a telnet app which sets the `$DISPLAY` variable. Chances are you’re using iTerm in which case you will have to manually declare the variable:

```bash
export DISPLAY=:0
# if this were SSH, then you'd do this:
# ssh -X <hostname>
```

Finally, you can use the freerdp client:

```bash
xfreerdp /u:youruser /p:yourpassword /v:hostnameoripaddr
```

## References and Further Reading

- [Using x11 apps in mac os x](https://medium.com/@toja/using-x11-apps-in-mac-os-x-c74b304fd128)
