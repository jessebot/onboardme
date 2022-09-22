# OnBoardMe
A project to store config files, as well as programatically install core packages accross several package managers that I need for development. A lot of this was amassed from many years of quickly looking into a thing™️ , jotting it down, and then just hoping I'd remember why it was there later, so this is now a renewed effort in remembering all the thing™️s, and automating as much as possible. The idea is that it's faster, smaller, and easier to configure than it's ansible equivalent. Here's an example of the terminal after the script has run:

<img src='./screenshots/terminal_screenshot.png' width='800'>

And here's an example of the cli:
```
# ./onboardme.py --help
usage: onboardme.py [-h] [--delete] [-e EXTRA [EXTRA ...]] [-f] [-i INSTALLERS [INSTALLERS ...]] [-r] [-H HOST [HOST ...]]

Onboarding script for macOS and debian. Uses config in the script repo in package_managers/packages.yml. If run with no options on
Linux it will install brew, apt, flatpak, and snap packages. On mac, only brew.

options:
  -h, --help            show this help message and exit
  --delete              Deletes existing rc files before creating hardlinks. BE CAREFUL!
  -e EXTRA [EXTRA ...], --extra EXTRA [EXTRA ...]
                        Extra package groups to install. Accepts multiple args, e.g. --extra gaming
  -f, --firefox         Opt into experimental firefox configuring
  -i INSTALLERS [INSTALLERS ...], --installers INSTALLERS [INSTALLERS ...]
                        Installers to run. Accepts multiple args, e.g. only run brew and apt: --installers brew apt
  -r, --remote          Setup SSH on a random port and add it to firewall.
  -H HOST [HOST ...], --host HOST [HOST ...]
                        Add IP to firewall for remote access
```

Currently in beta :3 Tested on macOS Monterey 12.4-12.5, and Debian 11 (Bullseye). Please report 🐛 in the GitHub issues, and I will get them as I have time. You can also open a pull request, and I can review it :blue_heart:

Looking for a project to get a fresh OS entirely, on a machine that has no OS? Check out [pxeless](https://github.com/cloudymax/pxeless).

Actually looking for a project to get started with self hosting k8s stuff? Check out [smol k8s homelab](https://github.com/jessebot/smol_k8s_homelab).

## Quick Start
[Get Started here :blue_heart:!](https://jessebot.github.io/onboardme/onboardme/quickstart)

## Under the hood
- Installs files are in the directory `configs/rc_files`: `.bashrc` files, `.vimrc`, `.zshrc`, and `.hyper.js`.
- Installs apt, snap, and flatpak packages from `./configs/installers/packages.yml`
- Installs gaming related packages via apt if you pass in `--extras gaming`.
- Installs brew files from `./configs/installers/brew/Brewfile_*` depending on OS
- Installs vim-plug, a vim plugin manager to setup things like nerdtree, indentations lines, and fuzzysearch
- Configures iptables to block traffic on most ports except for HTTPS as well as ICMP/SSH for a single IP

If you want to see the exact packages being installed, you can check out `configs/installers/packages.yml` for an easy to absorb yaml list of packages per installer. I bias towards brew fo cross-platform usage, and those packages are avavailble as Brewfiles in `configs/installers/brew/`.

### Current Ecoscape of Personal Tech

Category | App | Replaces
|:---:|:---:|:---:|
| Backups - local  | Restic to minio                       | Google Drive, iCloud                |
| Backups - remote | Restic to b2                          | Google Drive, iCloud, S3            |
| Email            | Protonmail and Bridge for Linux/MacOS | Gmail                               |
| Launcher         | ???                                   | Alfred                              |
| File Storage     | NextCloud Files/Photos                | Google Photos/Drive                 |
| Passwords        | Bitwarden                             | LastPass                            |
| News - RSS       | Fluent Reader                         | Facebook/Twitter news company feeds |
| Internet Videos  | FreeTube,Peertube                     | YouTube (Google)                    |

#### Docs
You can find the bulk of my notes under the `docs/` directory in this repo, but I've also recently setup a justthedocs page [here](https://jessebot.github.io/onboardme/).

## Important Notes on FOSS and Ethics
Here at this humble OnBoardMe repo, we try really hard to do the right thing. We're doing our best to get off of the giants like Google, Microsoft, Apple, Amazon, Samsung, etc... but we've still got a long way to go! Check back here for alternatives as we go on the journey ourselves! We'll link back to any orgs or projects we learn about, but feel free to open an issue with anything else we should link back to. :)

  *Living ethically under late stage capitalism is not easy, but we believe generally that software should be [Free and Open Source](https://www.gnu.org/philosophy/free-sw.en.html).*

#### Humane Tech Lists
We've had good luck with [Awesome Humane Tech](https://github.com/humanetech-community/awesome-humane-tech) for guides and checking out alternatives to tech from the Giants you previously used.

#### Language
We are currently using the philosophy of this RFC draft:
[Terminology, Power, & Exclusionary Language...](https://datatracker.ietf.org/doc/html/draft-knodel-terminology-09)

### Tips
Contact your local datacenters and see if they offer an object storage service, because they might, and it could be really cheap. Don't give your money to AWS, Microsoft, or Google.

### Special Thanks
Thank you to @cloudymax for all their direct contributions for gaming on Linux, virtualization, and the hyper terminal configs. Also great engineer to rubberduck with generally. Couldn't have polished a lot of this without their patience during my late night ramblings about my 8 different package managers and why utf-8 isn't called utf-14 :3 :blue_heart:
