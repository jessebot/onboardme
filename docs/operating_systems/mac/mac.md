---
layout: default
parent: Operating Systems
title: macOS
permalink: /os/macos
---

## Emojis
Mac Emoji Keyboard Shortcut: control + cmd + space

## Using modern `bash` on macOS
macOS ships with BASH 3.x, and that's pretty behind, so we generally always upgrade it, and then set a few things.

```bash
brew install bash
```

Whereever `brew` installs bash for you, set that in `/etc/shells`, so in our case, we get:

```bash
# add your new bash path to the acceptable shells list
sudo echo "/usr/local/bin/bash" >> /etc/shells

# set your shell for your user to the shell you echoed above
chsh -s /usr/local/bin/bash $(whoami)
```

### Disable BASH `chsh` warning

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

## iTerm2

```bash
# the dynamic profiles are stored here
ls ~/Library/Application Support/iTerm2/DynamicProfiles
```

## Awesome Lists
- [Awesome Mac](https://wangchujiang.com/awesome-mac/) has a list of like every tool you care about for every category, and has a good system to determine which things are FOSS vs Free vs Paid.

- [Awesome macOS open source applications](https://github.com/serhii-londar/open-source-mac-os-apps) is just open source stuff, skipping the app store all together, hopefully. I haven't verified everything.
