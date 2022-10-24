---
layout: default
title: Getting Started
parent: onboardme
permalink: /onboardme/getting-started
---

# Quick Start

If you haven't already, please refer to the
[install instructions](https://jessebot.github.io/onboardme/onboardme/installation).

You can run `onboardme` with no options or further configuration, and it will
not overwrite anything, but it will install packages and attempt to configure
fonts, vim, and give you further instructions to setup your machine on your own.

See below for configuration with cli options or a config file :)

## Configuration

### CLI

For the full help, you can check out the `--help` option. If anything there is
unclear, please feel free to open up [an issue](https://github.com/onboardme/issues)
and we can clear it up for you and make the help text, more helpful :)

```bash
onboardme --help
```

<details>
  <summary>Full Help Text</summary>

  [<img src='https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/help_text.svg' alt='screenshot of full output of onboardme --help'>](https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/help_text.svg)

</details>

### Config files

`onboardme` uses a `config.yaml` in its installation directory that has defaults.
Those defaults can be altered per machine by creating a config file like:

<details>
  <summary>`~/.config/onboardme/config.yml`</summary>

  ```yaml
  ---
  # ______________________________________________________________ #
  #         Config file for the onboardme cli command.             #
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
  #   - If this files exists as: ~/.config/onboardme/config.yml    #
  #     then its loaded instead of the default config              #
  # -------------------------------------------------------------- #
  
  
  log:
    # Full path to a file you'd like to log to. Creates file if it doesn't exist
    file: ""
    # what level of logs to output (debug,info, warn, error)
    level: "INFO"
    # don't output anything to the console, if set and log file passed in, still
    # creates a log file
    quiet: false
  
  
  # steps refer to a specific function in the list of functions we run
  steps:
    # these are mac specific steps
    Darwin:
      - vim_setup
      - dot_files
      - manage_pkgs
    # these are linux specific steps
    Linux:
      - vim_setup
      - dot_files
      - manage_pkgs
  
  
  dot_files:
    # personal git repo URL for your dot files, defaults to jessebot/dot_files
    git_url: "https://github.com/jessebot/dot_files.git"
    # the branch to use for the git repo above, defaults to main
    git_branch: "main"
    # !CAREFUL: runs a `git reset --hard`, which will overwite/delete files in ~
    # that conflict with the above defined git repo url and branch.
    # You should run the following to get the files that would be overwritten:
    # onboardme -s dot_files
    overwrite: false
  
  
  # this is the basic package config. to edit the specific packages, edit
  # ~/.config/onboardme/packages.yml
  package:
    # Remove any of the below pkg managers to only run the remaining pkg managers
    managers:
      - brew
      - pip3.10
      - snap
      - flatpak
      - apt
    # list of extra existing packages groups to install
    groups:
      - default
      # uncomment these to add them as default installed package groups
      # - gaming
      # - work
  
  
  # known safe remote hosts that you expect to be able to ping and SSH into
  remote_hosts: []
    # - 192.168.42.42
  
  # setup iptable on Linux only
  firewall: false
  
  
  ### TODO: make this work, it's a nice dream though.
  # any URL we can curl to download a folder from
  # wallpapers_download_url: ""
  ```

  If the comments in this configuration file are unclear, please feel free to 
  open up [an issue](https://github.com/onboardme/issues) and we'll help! :)

</details>

We also use a few package files, namely `packages.yml` and a couple of Brewfiles.

<details>
  <summary>`~/.config/onboardme/packages.yml`</summary>

  ```yaml
  ---
  apt:
    emoji: "🙃"
    commands:
      list: "apt list --installed"
      install: "sudo apt-get install -y "
      update: "sudo apt-get update -y"
      upgrade: "sudo apt-get upgrade -y"
    packages:
      default:
        - terminator
        - openssl
        - sysstat
        - silversearcher-ag
        # this should let you use the a yubikey for auth
        - libpam-yubico
        - finger
        - ssh
        # - nextcloud-desktop
        - screen
        - youtube-dl
        - bash-completion
        # networking
        - iptables
        - gufw
        - net-tools
        # package managers installing package managers... this is terrible.
        - snapd
        - flatpak
        - gnome-software-plugin-flatpak
        # cat images in the terminal :) works in tmux
        - catimg
        # this lets you ls images as thumbnails, which is helpful sometimes
        - imagemagick
        # pretty syntaxhighlighted cat files with git diff support
        - batcat
        # print a very pretty pallete to see all the colors the terminal can render
        - colortest
      gaming:
        - lutris
        - winehq-staging
        - steam
        # to format disks to exFAT; FAT is too thin for modern windows 10 ISOs
        # - exfat-utils
  
  flatpak:
    emoji: "🫓 "
    commands:
      setup: "sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo"
      list: "flatpak list --columns=application"
      install: "sudo flatpak install -y flathub "
    packages:
      default:
        - "org.freedesktop.Platform/x86_64/21.08"
        # youtube alternative
        - io.freetubeapp.FreeTube
        # password manager
        - com.bitwarden.desktop
  
  snap:
    emoji: "🫰 "
    commands:
      list: "snap list"
      install: "sudo snap install "
    packages:
      default:
        - core
        # rss feed reader
        - fluent-reader
        # screen debugger/sharing tool for android
        - scrcpy
  
  # most of this is actually for powerline, my shell prompt
  pip3.10:
    emoji: "🐍"
    commands:
      list: "pip3.10 list"
      install: "pip3.10 install --upgrade "
    packages:
      default:
        # this is for python development
        - pip
        - build
        - twine
        - autoimport
        # this is all powerline
        - powerline-status
        - powerline-gitstatus
        - powerline-kubernetes
        # for the internal ip address powerline shell prompt
        - netifaces
        # supposed to work with powerline for spotify info
        - dbus
        # this does some magic with imports when developing
  ```

</details>


## Config Sections and Explanations
### Steps
Steps refer to a specific function in the list of functions we run and can be
configured for both macOS and Linux seperately. These steps include:

- setting up dot files in your home directory (.bashrc, .vimrc, etc)
- setting up vim (installing vim-plug and vim plugins)
- managing packages using package managers (brew, pip3.10, apt, snap, flatpak)

They can be configured via the `steps` parameter in the `config.yml` above,
or via the the cli like:

```bash
# this runs only the dot_file management step
onboardme -s dot_files
```

or for multiple steps:

```bash
# this runs both the dot_file management step and the vim setup step
onboardme -s dot_files -s vim_setup
```

If you try to run a step that requires another step, we will automatically run
that step so for instance, to set up vim, we need dot files. e.g.

This command: `onboardme -s vim_setup`

In the background becomes: `onboardme -s dot_files -s vim_setup`

### dot files
The dot files for your home directory are installed from a git URL and branch
that you can configure either via the config file, or the cli. If your local
files conflict with the files in the repo, we will not overwrite them by default.
If you always want your local dot files overwritten, you can pass in the `-O` switch
or `--overwrite` option or set `overwrite` in your local `~/.config/onboardme/config.yml`.

```bash
# run onboardme with a custom git url and branch that overwrites existing files
onboardme --git_url git@github.com:jessebot/dot_files.git --git_branch main --overwrite
```

### packages
All of the packages are installed using package managers, and each package
manager has groups of packages they can install. You can specify specific
package managers and package groups via the `config.yml` file, or via the cli.

```bash
# only run the brew package manager and only use the devops package group
onboardme -p brew -g devops
```
