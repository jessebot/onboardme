---
layout: default
title: Quick Start
parent: onboardme
permalink: /onboardme/quickstart
---

## OnBoardMe Quick Start

First, make sure you have curl, but it *should* be there **already be on macOS**:

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

```zsh
# Download the setup.sh; you may have to install curl, see above codeblock
curl -O https://raw.githubusercontent.com/jessebot/onboardme/main/setup.sh
# give it execute permissions
chmod 0500 ./setup.sh
```

### macOS
macOS uses zsh as the default shell, and I don't currently support zsh, so type bash to get this ancient verison of bash to run the setup and onboardme, which will install a current version of bash. **The script will *not* run properly in zsh**.

```bash
bash
```

## run the setup.sh script
This is to install dependencies and clone the onboardme repo.

```bash
# NOTE THE . before the script! *Very* important!
. ./setup.sh

# just in case you didn't run the above script with .
source ~/.bash_profile || source ~/.bashrc
```

Now you can run the actual script that does the heavy lifting. If you can `setup.sh` above without errors, it will be installed in `~/repos/onboardme`:

```bash
# This will display a help
./repos/onboardme/onboardme --help

# this will run the script with no options
./repos/onboardme/onboardme
```

When the script completes, it'll output a number of other steps to take manually that aren't yet, or can't be, automated.

:partying_face: You're done :D
