---
layout: default
title: onboardme
nav_order: 2
has_children: true
permalink: /onboardme
---

## ☁️  onboard**me** 💻
[<img src='https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/help_text.svg' alt='screenshot of full output of onboardme --help'>](https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/help_text.svg)

This is [a project](https://github.com/jessebot/onboardme) to store config files, as well as programatically install core packages across several package managers that I need for development. A lot of this was amassed from many years of quickly looking into a thing™️ , jotting it down, and then just hoping I'd remember why it was there later, so this is now a renewed effort in remembering all the thing™️s, and automating as much as possible. The idea is that it's faster, smaller, and easier to configure than it's ansible equivalent. Here's an example of the terminal after the script has run:

<img src='https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/terminal_screenshot.png' width='850' alt='screenshot of terminal after running onboardme. includes colortest-256, powerline prompt, icons for files in ls output, and syntax highlighting examples with cat command.'>

## Under the hood

| Step                                 | Config Location in repo                  | OS            |
|--------------------------------------|------------------------------------------|---------------|
| Git fetch dot files                  | n/a: fetched from a configured git repo  | macOS/Debian  |
| Installs apps using package managers | `./onboardme/config/packages.yaml`        | Debian, macOS |
| Installs OPTIONAL apps               | `./onboardme/config/packages.yaml`        | Debian        |
| Installs fonts                       | n/a                                      | macOS/Debian  |
| Installs vim-plug + vim plugins      | plugins fetched from configured git repo | macOS/Debian  |
| Installs packer.nvm + neovim plugins | plugins fetched from configured git repo | macOS/Debian  |
| Adds user to the docker group        | n/a                                      | Debian        |


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

[Bitwarden]: https://bitwarden.com/ "bitwarden"
[Cerebro]: https://cerebroapp.com/ "cerebro"
[ClamAV]: https://www.clamav.net/ "clamav"
[Firefox]: https://www.mozilla.org/en-US/firefox "firefox"
[Fluent Reader]: https://hyliu.me/fluent-reader/ "fluent reader"
[FreeTube]: https://freetubeapp.io "freetube"
[LibreOffice]: https://www.libreoffice.org/ "libreoffice"
[Lulu]: https://objective-see.org/products/lulu.html "lulu"
[NeoVim]: https://neovim.org/ "neovim"
[NextCloud]: https://nextcloud.com/ "nextcloud"
[Restic]: https://restic.net/ "restic"
[Vim]: https://www.vim.org/ "vim"
[w3m]: https://w3m.sourceforge.net/ "w3m"
