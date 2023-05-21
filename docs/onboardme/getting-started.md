---
layout: default
title: Getting Started
parent: onboardme
has_children: true
permalink: /onboardme/getting-started
---

# Quick Start

If you haven't already, please refer to the
[install instructions](https://jessebot.github.io/onboardme/onboardme/getting-started/installation) 🌱.

You can run `onboardme` with no options or further configuration, and it will
not overwrite anything, but it will install packages and attempt to configure
fonts, neovim, and give you further instructions to setup your machine on your own.

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

`onboardme` uses a `config.yml` in its installation directory that has defaults.
Those defaults can be altered per machine by creating a config file like:

<details>
  <summary><code>~/.config/onboardme/config.yml</code></summary>

  ```yaml
  ---
  # ______________________________________________________________ #
  #         Config file for the onboardme cli:                     #
  #          ~/.config/onboardme/config.yml                        #
  # -------------------------------------------------------------- #

  log:
    # Full path to a file you'd like to log to. Creates file if it doesn't exist
    file: ""
    # what level of logs to output (DEBUG, INFO, WARN, ERROR)
    level: "INFO"

  # steps refer to a specific function in the list of functions we run
  steps:
    # these are mac specific steps
    Darwin:
      - dot_files
      - packages
      - font_setup
      - neovim_setup
    # these are linux specific steps
    Linux:
      - dot_files
      - packages
      - font_setup
      - neovim_setup
      - group_setup

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

  # This is the basic package config.
  package:
    # Remove any of the below pkg managers to only run the remaining pkg managers
    managers:
      # these are macOS specific steps
      Darwin:
        - brew
        - pip3.11
      # these are linux specific steps
      Linux:
        - brew
        - pip3.11
        - apt
        - snap
        - flatpak
    # list of extra existing packages groups to install
    groups:
      - default
      # uncomment these to add them as default installed package groups
      # - gaming
      # - work

  # known safe remote hosts that you expect to be able to ping and SSH into
  remote_hosts: []
    # has to be IP address or hostname like this example
    # - 192.168.42.42

  # setup iptable on Linux only
  firewall: false
  ```

  If the comments in this configuration file are unclear, please feel free to
  open up [an issue](https://github.com/onboardme/issues) and we'll help! :)

</details>

We also use a package file called
[`packages.yml`](https://github.com/jessebot/dot_files/blob/main/.config/onboardme/packages.yml)
which you can also place in your `~/.config/onboardme` directory, to take
precedence over our defaults.

## Config Sections and Explanations
### Steps
Steps refer to a specific function in the list of functions we run and can be
configured for both macOS and Linux seperately. These steps include:

- setting up dot files in your home directory (.bashrc, etc)
- managing packages using package managers (brew, pip3.11, apt, snap, flatpak)
- installing fonts
- setting up basic TUI IDE, neovim (vim is optional)
- setting up groups

They can be configured via the `steps` parameter in the `config.yml` above,
or via the the cli like:

```bash
# this runs only the dot_file management step
onboardme -s dot_files
```

or for multiple steps:

```bash
# this runs both the dot_file management step and the neovim setup step
onboardme -s dot_files -s neovim_setup
```

If you try to run a step that requires another step, we will automatically run
that step so for instance, to set up neovim, we need dot files. e.g.

This command: `onboardme -s neovim_setup`

In the background becomes: `onboardme -s dot_files -s neovim_setup`

### dot files
The dot files for your home directory are installed from a git URL and branch
that you can configure either via the config file, or the cli. If your local
files conflict with the files in the repo, we will not overwrite them by default.
If you always want your local dot files overwritten, you can pass in the `-O` switch
or `--overwrite` option or set `overwrite` in your local `~/.config/onboardme/config.yml`.

### `onboardme` cli
```bash
# run onboardme with a custom git url and branch that overwrites existing files
onboardme --git_url https://github.com/jessebot/dot_files.git --git_branch main --overwrite
```

### `config.yml`

```yaml
dot_files:
  git_url: "https://github.com/jessebot/dot_files.git"
  git_branch: "main"
  overwrite: true
```


### Package Management
All of the packages are installed using package managers, and each package
manager has groups of packages they can install. You can specify specific
package _managers_ and package _groups_ via the `config.yml` file, or via the cli.

By default, we install the `default` package _groups_ for all package _managers_.
This includes everything you need for a basic cli experience and a slim ide.

The default package managers for macOS and Linux are: `brew` and `pip3.11`

For Linux, we also include: `apt`, `snap`, and `flatpak`

See the examples below:

#### Install the "default" and "gui" package groups
This would install the default packages for the basic cli experience and a
slim ide PLUS GUI tools, like vlc and freetube.

##### `onboardme` cli

```bash
# can also be: onboardme -g default -g gui
onboardme --pkg_groups default --pkg_groups gui
```

##### `config.yml`

```yaml
package:
  groups:
    - default
    - gui
```

#### _Only_ install the "devops" package group for _only_ the `brew` package manager
This will install only additional tooling for devops work.
_Note: This will not install/upgrade the default package group._

##### `onboardme` cli

```bash
# can also be: onboardme -p brew -g devops
onboardme --pkg_managers brew --pkg_groups devops
```

##### `config.yml`

```yaml
package:
  managers:
      Darwin:
        - brew
      Linux:
        - brew
  groups:
    - devops
```
