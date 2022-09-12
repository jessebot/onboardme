---
layout: default
title: macOS
permalink: /macos
---

## Emojis
Mac Emoji Keyboard Shortcut: control + cmd + space

## Disable BASH `chsh` warning

Add the following to your BASH profile:
```bash
export BASH_SILENCE_DEPRECATION_WARNING=1
```

## Finder
you can run
```
defaults write com.apple.finder QuitMenuItem -bool YES && killall
```

Finder command in the Terminal, after that you can exit Finder with ⌘Q just like any other app. It won't help to remove Finder from the Dock though.

To revert, run:
```
defaults write com.apple.finder QuitMenuItem -bool NO && killall Finder
```

This is such a pain, right? Why does mac want its dock to look so cluttered?

https://github.com/jesscxc/hide-finder-trash-dock-icons

## here's some lists I found
- [Awesome Mac](https://wangchujiang.com/awesome-mac/) has a list of like every tool you care about for every category, and has a good system to determine which things are FOSS vs Free vs Paid.

- [Awesome macOS open source applications](https://github.com/serhii-londar/open-source-mac-os-apps) is just open source stuff, skipping the app store all together, hopefully. I haven't verified everything.

## TouchiD for sudo auth:

Add `auth sufficient pam_tid.so` to line 2 of `/etc/pam.d/sudo`

Example:

```bash
# sudo: auth account password session
auth       sufficient     pam_tid.so
auth       sufficient     pam_smartcard.so
auth       required       pam_opendirectory.so
account    required       pam_permit.so
password   required       pam_deny.so
session    required       pam_permit.so
```
