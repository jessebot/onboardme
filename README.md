# OnBoardMe
A project to store config files, as well as programatically install core packages across several package managers that I need for development. A lot of this was amassed from many years of quickly looking into a thing™️ , jotting it down, and then just hoping I'd remember why it was there later, so this is now a renewed effort in remembering all the thing™️s, and automating as much as possible. The idea is that it's faster, smaller, and easier to configure than it's ansible equivalent. Here's an example of the terminal after the script has run:

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

Currently in beta :3 Tested on macOS Monterey 12.5-12.6, and Debian 11 (Bullseye). Please report 🐛 in the GitHub issues, and I will get them as I have time. You can also open a pull request, and I can review it :blue_heart:

Looking for a project to get a fresh OS entirely, on a machine that has no OS? Check out [pxeless](https://github.com/cloudymax/pxeless).

Actually looking for a project to get started with self hosting k8s stuff? Check out [smol k8s homelab](https://github.com/jessebot/smol_k8s_homelab).

## Quick Start
[Get Started here :blue_heart:!](https://jessebot.github.io/onboardme/onboardme/quickstart)

#### Docs
You can find the bulk of my notes under the `docs/` directory in this repo, but I've also recently setup a justthedocs page [here](https://jessebot.github.io/onboardme/).

### Special Thanks
Thank you to @cloudymax for all their direct contributions for gaming on Linux, virtualization, rc file edits, and the hyper terminal configs. Also great engineer to rubberduck with generally. Couldn't have polished a lot of this without their patience during my late night ramblings about my 8 different package managers and why utf-8 isn't called utf-14 :3 :blue_heart:

### Status
Currently in beta :3 Testing actively on macOS Monterey 12.6, and Debian 11 (Bullseye). Please report 🐛 in the GitHub issues, and I will get them as I have time.
