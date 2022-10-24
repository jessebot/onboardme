---
layout: default
title: Installation
parent: onboardme
permalink: /onboardme/installation
---

# OnBoardMe Installation

## Prerequisites

<details>
  <summary>curl</summary>

  ```bash
  # First, make sure you have curl, but it *should* be there already be on macOS.
  # if this doesn't return anything, you need to install curl
  which curl
  
  # Debian/Ubuntu
  sudo apt install -y curl
  ```

  If it's not there on Linux, you can install it with `apt` or use any default package manager like yum, or whatever people who use gentoo use

</details>

Now you can run the `setup.sh` script, or manually install the remaining prereqs.

<details>
  <summary>`setup.sh` script</summary>

  Download and run the setup script to install git, brew, python, and python dependencies. The `setup.sh` will ask for your password to install things. Run the following from your home directory:

  ```bash
  # macOS uses zsh as the default shell, type bash to get this ancient verison
  # of bash to run the setup and and then onboardme, which will install a 
  # current version of bash. **The script will *not* run properly in zsh**.
  chsh -s /bin/bash
  bash

  # Download the setup.sh; you may have to install curl, see above codeblock
  curl -O https://raw.githubusercontent.com/jessebot/onboardme/main/setup.sh

  # give it execute permissions
  chmod 0500 ./setup.sh

  # NOTE THE . before the script! *Very* important!
  . ./setup.sh

  # just in case you didn't run the above script with .
  source ~/.bash_profile || source ~/.bashrc
  ```

  If you finished the steps above, you can jump down to the [Actual installation](#actual-installation) section 😃

</details>


<details>
  <summary>brew</summary>

  As per the [brew](https://brew.sh) documentation:

  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
  
</details>

<details>
  <summary>Python3.10</summary>

  This is a test of every markdown style I know.

  ```bash
    brew install python@3.10
  ```

</details>


## Actual installation

Recently, I started moving to actually package this, so you should be able to
do:
```bash
pip3.10 install onboardme
```

## Quick test of `onboardme`
Now you can run the actual script that does the heavy lifting. If you ran the
above `setup.sh` and `pip install` without errors, you can start using
`onboardme` now:

```bash
# This will display a help
onboardme --help
```

🎉 You're done! We're so proud of you. 🥹
_(and not in a sarcastic way, like we legitmately are proud of you for getting thorugh this awful alpha project doc)_

Now head over to the [Quickstart](https://jessebot.github.io/onbaordme/getting-started#quickstart)
to get rolling!
