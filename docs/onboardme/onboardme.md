---
layout: default
title: onboardme.py
nav_order: 2
has_children: true
permalink: /onboardme
---

# OnBoardMe
A [A project](https://github.com/jessebot/onboardme) to store config files, as well as programatically install core packages across several package managers that I need for development. A lot of this was amassed from many years of quickly looking into a thing™️ , jotting it down, and then just hoping I'd remember why it was there later, so this is now a renewed effort in remembering all the thing™️s, and automating as much as possible. The idea is that it's faster, smaller, and easier to configure than it's ansible equivalent. Here's an example of the terminal after the script has run:

<img src='https://raw.githubusercontent.com/jessebot/onboardme/main/screenshots/terminal_screenshot.png' width='800'>

And here's an example of the cli:
<img src='https://raw.githubusercontent.com/jessebot/onboardme/main/screenshots/help_text.png' width='800'>

Looking for a project to get a fresh OS entirely, on a machine that has no OS? Check out [pxeless](https://github.com/cloudymax/pxeless).

## Under the hood

|       Step                                  | Config Location in repo | OS           |
|:---:|:---:|:---:|
| Installs fonts                              | n/a                     | macOS/Debian |
| Installs dot files                          | `configs/dot_files`     | macOS/Debian |
| Installs brew/pip3.10 packages              | `./package_managers/brew/Brewfile_standard`, `./package_managers/brew/Brewfile_$OS`, `./package_managers/pip3.10/requirements.txt` | macOS/Debian |
| Installs apt, snap, flatpak packages        | `./package_managers/packages.yml`     | Debian |
| Installs gaming related packages via apt if you pass in `--extras gaming`. | `./package_managers/packages.yml` | Debian |
| Installs vim-plug, a vim plugin manager  | `configs/dot_files/.vimrc` | macOS/Debian
| Configures iptables to block traffic on most ports except for HTTPS as well as ICMP/SSH for a single IP | `configs` | Debian |
| Setups up iTerm2 fonts and colors | `configs/iterm2` | macOS |
| Adds user to the docker group | n/a | Debian |

### Current Ecoscape of Personal Tech

These are all Linux Desktop and macOS applications I use. 
OnBoardMe doesn't officially support phones yet, but for what I use on my phone, check out my [doc](/onboardme/os/android).

| Category | App | Replaces |
|:---:|:---|:---|
| Backups - local/remote | Restic to minio and b2              | GDrive, iCloud, S3                |
| Web Browser            | Firefox, Lynx/w3m (terminal only)   | Chrome/Safari/Edge                |
| Email Client           | Thunderbird + Protonmail + Bridge for Linux/MacOS | Gmail               |
| IDE                    | Vim + Plugins                       | Vscode/JetBrains/etc              |
| Document Editor        | LibreOffice                         | Microsoft Word                    |
| Launcher               | Undecided                           | Alfred                            |
| Photo/file Storage     | NextCloud Files/Photos (testing)    | Google Photos/Drive               |
| Passwords              | Bitwarden                           | LastPass, Apple/Google            |
| News - RSS             | Fluent Reader                       | Facebook/Twitter/news/brand feeds |
| Video                  | FreeTube, Peertube                  | YouTube                           |
| Antivirus              | ClamAV                              | MalwareBytes                      |


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
