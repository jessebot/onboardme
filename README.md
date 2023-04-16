<h2 align="center">
  <img
    src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png"
    height="30"
    width="0px"
  />
  💻 onboard<i>me</i>
  <img
    src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png"
    height="30"
    width="0px"
  />
</h2>
<p align="center">
  <a href="https://github.com/jessebot/onboardme/releases">
    <img src="https://img.shields.io/github/v/release/jessebot/onboardme?style=plastic&labelColor=484848&color=3CA324&logo=GitHub&logoColor=white">
  </a>
</p>

Get your daily driver just the way you like it, from dot files installation, to package installation, to other little features you didn't know you needed, `onboardme` intends to save you time with initializing and upgrading your environment.

## Features

### Keep your Dot Files Up To Date Across multiple systems
`onboardme` can manage your [dot files] using a git by turning your home directory into a repo.

<details>
  <summary>We provide default dot files, so you don't have to manage them</summary>

- The [default dot files] are open source, and the maintainers use these themselves
- They cover a lot of common apps/tools you probably want anyway
- They have consistent colorschemes accross different CLI/TUI programs 😃
- They set all the helpful BASH aliases you could need (zsh support coming soon)

</details>

### Package management
We install and upgrade libraries and apps using common package managers.

<details>
  <summary>onboardme provides a currated list of default packages</summary>
  
- checkout the [default packages]
- supports `brew`, `apt`, `snap`, `flatpak`, and `pip` (and you can add your own 😄)
- group together packages for different kinds of environments
  - onboardme provides default package groups:
    - default (no desktop GUI apps installed by default, always installed)
    - macOS (default apps for _macOS only_ apps, always installed on macOS)
    - gui (default GUI apps for Linux desktops, optionally installed)
    - devops (devops related tooling, optionally installed)

</details>

### NeoVim Plugin Installtion and Updates
onboardme keeps your neovim plugins installed and up to date with [lazy.nvim] under the hood.
  
<details>
  <summary>Why no vim though?</summary>
  
  If you haven't already made the switch from Vim to [NeoVim], you can try out NeoVim today with `onboardme` :D We used to support both neovim _and_ vim, but these days none of the primary developers of this repo use pure vim anymore, so we can't ensure it's up to standards. All of your knowledge from vim is still helpful in neovim though, and we highly recommend switching as neovim has a lot more features and a very active plugin community :) NeoVim maintains a guide on how to switch from vim [here](https://neovim.io/doc/user/nvim.html#nvim-from-vim). 

</details>

### Easy `yaml` config files
- [XDG Base Directory Spec] use for [config files](#configuration)
  - Uses `$XDG_CONFIG_HOME/onboardme/config.yml` and `$XDG_CONFIG_HOME/onboardme/packages.yml`

### Other useful (but optional) configurations
- Enable touchID for sudo on macOS
- Add your user to the docker group
- Install nerdfonts (defaults to Hack and Symbols Only)
- Set capslock to control (🚧 in the works)

### Screenshots

<details>
  <summary>Example of <code>onboardme --help</code></summary>

<p align="center" width="100%">
<a href="https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/help_text.svg">
<img src="./docs/onboardme/screenshots/help_text.svg" alt='screenshot of full output of onboardme --help'>
</a>
</p>

</details>

<details>
  <summary>Examples of the terminal after <code>onboardme</code> runs</summary>

<p align="center" width="100%">

### neovim
<img width="90%" src='https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/neovim_example_1.png' alt='screenshot of neovim with colors'>

### Powerline and ls
<img width="80%" src='https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/ls_tree_examples.png' alt='screenshot of powerline and lsd'>

### Powerline with git
<img width="90%" src='https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/git_powerline_example.png' alt='screenshot of powerline and git colors'>

### Image and colors
<img width="90%" src='https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/image_in_terminal.png' alt='screenshot of color samples and image of dog using a computer using sixel'>

### Python virtual env in powerline and cat
<img width="90%" src='https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/python_virtual_env_example.png' alt='screenshot of using bat and python virtual env in powerline'>
</p>

</details>

## Quick Start

### Installation
The quickest way to get started on a fresh macOS or distrubtion of Debian (including Ubuntu) is:

```bash
# this will download setup.sh to your current directory and run it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/jessebot/onboardme/main/setup.sh)"

# this will display the help text for the onboardme cli
onboardme --help
```

If you've already got brew and Python3.11 on your machine, you can just do:

```bash
# should also work with pipx, if you'd like to use that instead
pip install --user onboardme
```

You can read more in depth at the [Getting Started Docs] 💙! There's also more [docs] on basically every program that onboardme touches.

### Upgrades
If you're on python 3.11, you should be able to do:

```bash
pip3.11 install --upgrade onboardme
```

### Configuration
onboardme has lots of CLI options, but you can also use config files. You have to create these files for the time being.

Config files are in `~/.config/onboardme/` (will use `$XDG_CONFIG_HOME`, if defined). Examples below:

<details>
<summary><code>~/.config/onboardme/config.yml</code></summary>

```yaml
log:
  # Full path to a file you'd like to log to. Creates file if it doesn't exist
  file: ""
  # what level of logs to output (DEBUG, INFO, WARN, ERROR)
  level: "INFO"

# steps refer to a specific function in the list of functions we run
steps:
  # these are mac specific steps
  Darwin:
    # clones dot files into home dir/git fetches updates for dot files
    - dot_files
    # install packages
    - packages
    # adds nerdfonts
    - font_setup
    # runs :Lazy sync to install all your plugins
    - neovim_setup
    # sets up touchID for sudo
    - sudo_setup
  # these are linux specific steps
  Linux:
    - dot_files
    - packages
    - font_setup
    - neovim_setup
    # add your user to the docker group
    - group_setup

dot_files:
  # personal git repo URL for your dot files, defaults to jessebot/dot_files
  git_url: "https://github.com/jessebot/dot_files.git"
  # the branch to use for the git repo above, defaults to main
  git_branch: "main"
  # !CAREFUL: runs a `git reset --hard`, which will overwite/delete local files in ~ that
  # conflict with the above defined git repo url and branch. You should run
  # `onboardme -s dot_files` to get the files that would be overwritten
  overwrite: false

# basic package config
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
    # - gui
    # - gaming
    # - devops
```

</details>

## Under the Hood
Made and tested for these operating systems:

[![Tested on Ventura with an M1 and older generation](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white)](https://wikiless.org/wiki/MacOS?lang=en)
[![Tested only on Debian Bookworm](https://img.shields.io/badge/Debian-A81D33?style=for-the-badge&logo=debian&logoColor=white)](https://www.debian.org/)
[![Tested only on ubuntu servers](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)

And optomized for the following programs:

[![made-with-neovim](https://img.shields.io/badge/NeoVim-0f191f?style=for-the-badge&logo=neovim&logoColor=#5c983b)](https://neovim.io/)
[![made-with-python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![made-with-bash](https://img.shields.io/badge/GNU%20Bash-000000?style=for-the-badge&logo=GNU%20Bash&logoColor=#5c983b)](https://www.gnu.org/software/bash/)
[![made-with-powerline](https://img.shields.io/badge/powerline-000000?style=for-the-badge&logo=powerline&logoColor=#5c983b)](https://powerline.readthedocs.io/en/master/overview.html)


#### Built using these great tools:

[<img src="https://github.com/textualize/rich/raw/master/imgs/logo.svg" alt="rich python library logo with with yellow snake" width="200">](https://github.com/Textualize/rich/tree/master)
[<img src="https://raw.githubusercontent.com/ryanoasis/nerd-fonts/master/images/nerd-fonts-logo.svg" width="120" alt="nerd-fonts: Iconic font aggregator, collection, and patcher">](https://www.nerdfonts.com/)


## Status
Still not production ready, but reasonably stable :)

Please report 🐛 in the GitHub issues, and we will collect them,
and release them back into the wild, because we are vegan and nice.
(Kidding, we will help! 😌)

We love contributors! Feel free to open a pull request, and we will review it asap! :)

:star: If you like this project, please star it to help us keep motivated :3

### Contributors

<!-- readme: contributors -start -->
<table>
<tr>
    <td align="center">
        <a href="https://github.com/jessebot">
            <img src="https://avatars.githubusercontent.com/u/2389292?v=4" width="100;" alt="jessebot"/>
            <br />
            <sub><b>JesseBot</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/cloudymax">
            <img src="https://avatars.githubusercontent.com/u/84841307?v=4" width="100;" alt="cloudymax"/>
            <br />
            <sub><b>Max!</b></sub>
        </a>
    </td></tr>
</table>
<!-- readme: contributors -end -->

## Shameless plugs for other projects
Get running on a machine using a bootable USB stick with [pxeless](https://github.com/cloudymax/pxeless).

Get started with virtual machines and QEMU with [scrap metal](https://github.com/cloudymax/Scrap-Metal).

Get started with testing kubernetes locally, even on metal with [smol k8s lab](https://github.com/jessebot/smol_k8s_lab).

<!-- link references -->
[documentation]: https://jessebot.github.io/onboardme/onboardme "onboardme documentation"
[default dot files]: https://github.com/jessebot/dot_files "default dot files for onboardme"
[help text]: https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/help_text.svg "an svg of the command: onboardme --help"
[Getting Started Docs]: https://jessebot.github.io/onboardme/onboardme/getting-started "getting started documentation"
[default packages]: https://github.com/jessebot/dot_files/blob/main/.config/onboardme/packages.yml "default installed packages for onboardme"

<!-- external link references -->
[dot files]: https://en.wikipedia.org/wiki/Hidden_file_and_hidden_directory#Unix_and_Unix-like_environments "wiki entry for dot file explanation"
[XDG Base Directory Spec]: https://specifications.freedesktop.org/basedir-spec/latest/ar01s03.html
[NeoVim]: https://neovim.io/ "neovim, vim improved"
[lazy.nvim]: https://github.com/folke/lazy.nvim "lazy.nvim, a plugin manager for neovim"
