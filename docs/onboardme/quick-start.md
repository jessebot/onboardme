---
layout: default
title: Quick Start
parent: onboardme.py
permalink: /onboardme/quickstart
---

## OnBoardMe Quick Start
First, make sure you have curl, but it *should* be there ***already be on macOS Monterey***:
```bash
# if this doesn't return anything, you need to install curl
which curl
```
If it's not there on Linux, you can install it with `apt` or use any default package manager like yum, or whatever people who use gentoo use
```bash
# Debian/Ubuntu
sudo apt install -y curl
```
Download and run the setup script to install git, brew, python, and python dependencies. The `setup.sh` will ask for your password to install things. Run the following from your home directory:
```bash
# Download the setup.sh; you may have to install curl, see above codeblock
curl -O https://raw.githubusercontent.com/jessebot/onboardme/main/setup.sh
# give it execute permissions
chmod 0500 ./setup.sh
# run the script, to install dependencies and clone the onboardme repo
. ./setup.sh
```

Now you can run the actual script that does the heavy lifting. If you can `setup.sh` above without errors, it will be installed in `~/repos/onboardme`:
```bash
# This will display a help
./repos/onboardme/onboardme.py --help

# this will run the script with no options
./repos/onboardme/onboardme.py
```

When the script completes, it'll output a number of other steps to take manually that aren't yet, or can't be, automated.

:party: You're done :D
