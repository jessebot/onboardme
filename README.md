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

Get your daily driver just the way you like it, from textformatting, and dot files to opensource package installation, onboardme intends to save you time with initializing or upgrading your environment.

### Features
- manage your [dot files] using a git repo (or use [our default dot files] 😃)
- install and upgrade libraries and apps
  - supports different several package managers and a couple of operating systems
  - can group together packages for different kinds of setups, e.g. gaming, devops, gui
- easy `yaml` config files in your `$HOME/.config/onboardme/` directory

#### Screenshots

<details>
  <summary>Example of <code>onboardme --help</code></summary>
  
<p align="center" width="100%">
<a href="https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/help_text.svg">
<img src="./docs/onboardme/screenshots/help_text.svg" alt='screenshot of full output of onboardme --help'>
</a>
</p>

</details>

<details>
  <summary>Example of the terminal after <code>onboardme</code> runs</summary>
  
<p align="center" width="100%">
    <img width="90%" alt="screenshot of terminal after running onboardme. includes colortest-256, powerline prompt, icons for files in ls output, and syntax highlighting examples with cat command." src="https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/terminal_screenshot.png">
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

You can also read more in depth [Getting Started Docs] 💙!

There's also more [documentation] on basically every program that onboardme touches.

### Upgrades
If you're on python 3.11, you should be able to do:

```bash
pip3.11 install --upgrade onboardme
```

### Configuration
onboardme has lots of CLI options, but you can also use config files. You have to create these files for the time being.

Config files are in `~/.config/onboardme/` (will use `$XDG_CONFIG_HOME`, if defined). Examples below:

<details>
<summary><code>config.yaml</code></summary>


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
    - dot_files
    - packages
    - font_setup
    - vim_setup
    - neovim_setup
    - sudo_setup
  # these are linux specific steps
  Linux:
    - dot_files
    - packages
    - font_setup
    - vim_setup
    - neovim_setup
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
    # - gaming
    # - devops
```

</details>

## Under the Hood

#### Made for the following OS (lastest stable):

[![made-for-macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white)](https://wikiless.org/wiki/MacOS?lang=en)
[![made-for-debian](https://img.shields.io/badge/Debian-A81D33?style=for-the-badge&logo=debian&logoColor=white)](https://www.debian.org/)
[![made-for-ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)

#### Optimized for:

[![made-with-for-vim](https://img.shields.io/badge/VIM-%2311AB00.svg?&style=for-the-badge&logo=vim&logoColor=white)](https://www.vim.org/)
[![made-with-python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![made-with-bash](https://img.shields.io/badge/GNU%20Bash-4EAA25?style=for-the-badge&logo=GNU%20Bash&logoColor=white)](https://www.gnu.org/software/bash/)

#### Built using these great projects:

[<img src="https://github.com/textualize/rich/raw/master/imgs/logo.svg" alt="rich python library logo with with yellow snake" width="200">](https://github.com/Textualize/rich/tree/master)
[<img src="https://raw.githubusercontent.com/ryanoasis/nerd-fonts/master/images/nerd-fonts-logo.svg" width="120" alt="nerd-fonts: Iconic font aggregator, collection, and patcher">](https://www.nerdfonts.com/)
- [powerline](https://powerline.readthedocs.io/en/master/overview.html)

## Status
Still not production ready, but reasonably stable :)

Please report 🐛 in the GitHub issues, and we will collect them,
and release them into the wild, because we are vegan and nice.
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
[dot files]: https://en.wikipedia.org/wiki/Hidden_file_and_hidden_directory#Unix_and_Unix-like_environments "wiki entry for dot file explanation"
[our default dot files]: https://github.com/jessebot/dot_files "default dot files for onboardme"
[help text]: https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/help_text.svg "an svg of the command: onboardme --help"
[Getting Started Docs]: https://jessebot.github.io/onboardme/onboardme/getting-started "getting started documentation"
[post screenshot]: https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/terminal_screenshot.png "screenshot of terminal afer onboardme"
