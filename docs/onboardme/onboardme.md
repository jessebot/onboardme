---
layout: default
title: onboardme
nav_order: 2
has_children: true
permalink: /onboardme
---

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
- easy `yaml` [config files](https://github.com/jessebot/onboardme#configuration) in your `$HOME/.config/onboardme/` directory

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
  <summary>Examples of the terminal after <code>onboardme</code> runs</summary>

<p align="center" width="100%">

### vim
<img width="90%" src='https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/vim_example_1.png' alt='screenshot of vim with colors'>

### Powerline and ls
<img width="90%" src='https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/ls_tree_examples.png' alt='screenshot of powerline and lsd'>

### Powerline with git
<img width="90%" src='https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/git_powerline_example.png' alt='screenshot of powerline and git colors'>

### Image and colors
<img width="90%" src='https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/image_in_terminal.png' alt='screenshot of color samples and image of dog using a computer using sixel'>

### Python virtual env in powerline and cat
<img width="90%" src='https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/python_virtual_env_example.png' alt='screenshot of using bat and python virtual env in powerline'>
</p>

</details>

Check out our [/onboardme/features](https://jessebot.github.io/onboardme/onboardme/features) page for more info on what we can do :)

## Under the hood

Here's the steps we take depending on what OS we run on. Each step can also be configured to be skipped.

| Step                                 | Config Location in repo                  |       OS      |
|:-------------------------------------|:-----------------------------------------|:-------------:|
| Git fetch dot files                  | n/a: fetched from a configured git repo  | Debian, macOS |
| Installs apps using package managers | `./onboardme/config/packages.yaml`       | Debian, macOS |
| Installs OPTIONAL apps, if any       | `./onboardme/config/packages.yaml`       | Debian, macOS |
| Installs fonts                       | n/a                                      | Debian, macOS |
| Installs vim-plug + vim plugins      | plugins fetched from configured git repo | Debian, macOS |
| Installs packer.nvm + neovim plugins | plugins fetched from configured git repo | Debian, macOS |
| Adds user to the docker group        | n/a                                      |     Debian    |
| Set sudo to use touchID              | n/a                                      |     macOS    |


### Current Ecoscape of Personal Tech

These are all Linux Desktop and macOS applications we use.
OnBoardMe doesn't officially support phones yet, but for what I, Jesse,
use on my phone, check out my [doc](/onboardme/os/android).

| Category               | App                                | Replaces                          |
|:-----------------------|:-----------------------------------|:----------------------------------|
| Backups - local/remote | [Restic] to minio and b2           | GDrive, iCloud, S3                |
| Web Browser            | [Firefox], [w3m] (terminal only)   | Chrome/Safari/Edge                |
| Email Client           | [NeoMutt], Protonmail + Bridge     | Gmail                             |
| IDE                    | [Vim]/[NeoVim] + Plugins           | Vscode/Pycharm etc                |
| Document Editor        | [LibreOffice]                      | Microsoft Word, Google Docs       |
| Launcher               | [Cerebro]                          | Alfred                            |
| Photo/file Storage     | [NextCloud] Files/Photos (testing) | Google Photos/Drive               |
| Passwords              | [Bitwarden]                        | LastPass, Apple/Google            |
| VPN                    | [WireGuard]                        | Cisco, OpenVPN(is FOSS, but old)  |
| News - RSS             | [Fluent Reader]                    | Facebook/Twitter/news/brand feeds |
| Video                  | [FreeTube], VLC                    | YouTube/Quicktime                 |
| Antivirus              | [ClamAV]                           | MalwareBytes                      |
| Firewall               | [Lulu]/iptables                    | ???                               |

## Important Notes on Ethics

### FOSS
Here at this humble OnBoardMe repo, we try really hard to do the right thing. We're doing our best to get off of the giants like Google, Microsoft, Apple, Amazon, Samsung, etc... but we've still got a long way to go! Check back here for alternatives as we go on the journey ourselves! We'll link back to any orgs or projects we learn about, but feel free to open an issue with anything else we should link back to. :)

  *Living ethically under late stage capitalism is not easy, but we believe generally that software should be [Free and Open Source](https://www.gnu.org/philosophy/free-sw.en.html). If we can't have that, we'll take as close as possible.*

#### Humane Tech Lists
We've had good luck with [Awesome Humane Tech](https://github.com/humanetech-community/awesome-humane-tech) for guides and checking out alternatives to tech from the Giants you previously used.

#### Language
We are currently using the philosophy of this RFC draft:
[Terminology, Power, & Exclusionary Language...](https://datatracker.ietf.org/doc/html/draft-knodel-terminology-10)

That same RFC also references a few tools you can use to fix your current environments, such as linters to be maintain inclusive language. TODO: pull them all and put them here.

### Tips
Contact your local datacenters and see if they offer an object storage service, because they might, and it could be really cheap. Don't give your money to AWS, Microsoft, or Google if you don't absolutely have to.

Looking for a project to get a fresh OS entirely, on a machine that has no OS?
Check out [pxeless](https://github.com/cloudymax/pxeless).
It works great in combination with onboardme :)

<!-- --------------- link references ---------------- -->

[Bitwarden]: https://bitwarden.com/ "bitwarden home page"
[Cerebro]: https://cerebroapp.com/ "cerebro home page"
[ClamAV]: https://www.clamav.net/ "clamav home page"
[Firefox]: https://www.mozilla.org/en-US/firefox "firefox home page"
[Fluent Reader]: https://hyliu.me/fluent-reader/ "fluent reader home page"
[FreeTube]: https://freetubeapp.io "freetube home page"
[LibreOffice]: https://www.libreoffice.org/ "libreoffice hom epage"
[Lulu]: https://objective-see.org/products/lulu.html "lulu home page"
[NeoVim]: https://neovim.org/ "neovim home page"
[NextCloud]: https://nextcloud.com/ "nextcloud home page"
[Restic]: https://restic.net/ "restic home page"
[Vim]: https://www.vim.org/ "vim home page"
[w3m]: https://w3m.sourceforge.net/ "w3m home page"
[WireGuard]: https://www.wireguard.com/ "wireguard home page"
