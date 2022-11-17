## ☁️  onboard**me** 💻

[![./docs/onboardme/screenshots/help_text.svg alt='screenshot of full output of onboardme --help](https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/help_text.svg)](https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/help_text.svg)

This is a project to store config files, as well as programatically install core packages across several package managers that we need for development. A lot of this was amassed from many years of quickly looking into a thing™️ , jotting it down, and then just hoping we'd remember why it was there later, so this is now a renewed effort in remembering all the thing™️s, and automating as much as possible. The idea is that it's faster, smaller, and easier to configure than it's ansible equivalent.

Here's an example of the terminal after the script has run:

[<img alt="screenshot of terminal after runnign onboardme. includes colortest-256, powerline prompt, icons for files in ls output, and syntax highlighting examples with cat command." width="750" src="https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/terminal_screenshot.png">](https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/terminal_screenshot.png)


## Quick Start
The quickest way to get started on a fresh macOS or Debian OS is:
```bash
# this will download setup.sh to your current directory and run it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/jessebot/onboardme/main/setup.sh)"

# this will display the help for the onboardme cli
onboardme --help
```
You can also read more in depth [Getting Started docs](https://jessebot.github.io/onboardme/onboardme/getting-started) 💙!


#### More Docs
We've recently setup a justthedocs page [here](https://jessebot.github.io/onboardme/).

### Upgrading
If you're on python3.11.0 or later, you should be able to do:
```bash
pip3.11 install --upgrade onboardme
```

## Features
Made for the following OS (lastest stable):

[![made-for-macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white)](https://wikiless.org/wiki/MacOS?lang=en)
[![made-for-debian](https://img.shields.io/badge/Debian-A81D33?style=for-the-badge&logo=debian&logoColor=white)](https://www.debian.org/)
[![made-for-ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)

Optimized for:

[![made-with-for-vim](https://img.shields.io/badge/VIM-%2311AB00.svg?&style=for-the-badge&logo=vim&logoColor=white)](https://www.vim.org/)
[![made-with-python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![made-with-bash](https://img.shields.io/badge/GNU%20Bash-4EAA25?style=for-the-badge&logo=GNU%20Bash&logoColor=white)](https://www.gnu.org/software/bash/)

And built using these great projects. Please go check them out:

[<img src="https://github.com/textualize/rich/raw/master/imgs/logo.svg" alt="rich python library logo with with yellow snake" width="200">](https://github.com/Textualize/rich/tree/master)
[<img src="https://raw.githubusercontent.com/ryanoasis/nerd-fonts/master/images/nerd-fonts-logo.svg" width="140" alt="nerd-fonts: Iconic font aggregator, collection, and patcher">](https://www.nerdfonts.com/)
- [powerline](https://powerline.readthedocs.io/en/master/overview.html)

## Status

🎉 Active project! Currently in later alpha :D (*But not yet stable. There be 🐛.*)

Please report 🐛 in the GitHub issues, and we will collect them,
and release them into the wild, because we are vegan and nice.
(Kidding, we will help! 😌)

We love contributors! Feel free to open a pull request, and we will review it asap! :)

:star: If you like this project, please star it to help us keep motivated :3

## Collaborators

<!-- readme: collaborators -start -->
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
<!-- readme: collaborators -end -->

## Shameless plugs for other projects
Looking for a project to get running on a machine that has no OS at all?
Check out [pxeless](https://github.com/cloudymax/pxeless).

Looking for a project to get started with self hosting k8s stuff?
Check out [smol k8s lab](https://github.com/jessebot/smol_k8s_lab).
