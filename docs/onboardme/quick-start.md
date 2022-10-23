---
layout: default
title: Quick Start
parent: onboardme
permalink: /onboardme/quickstart
---

# OnBoardMe Quick Start

## Prerequisites

<details>
        <summary>curl</summary>
        <pre>

        First, make sure you have curl, but it *should* be there already be on macOS.

        ~~~ bash
        # if this doesn't return anything, you need to install curl
        which curl
        ~~~

        If it's not there on Linux, you can install it with `apt` or use any default package manager like yum, or whatever people who use gentoo use

        ```bash
          # Debian/Ubuntu
          sudo apt install -y curl
        ```

        </pre>

</details>

From here, you can run my setup script, or you can manually install the
remaining prerequisites.

<details>
  <summary>`setup.sh`</summary>

  Download and run the setup script to install git, brew, python, and python dependencies. The `setup.sh` will ask for your password to install things. Run the following from your home directory:

  ```bash
  # Download the setup.sh; you may have to install curl, see above codeblock
  curl -O https://raw.githubusercontent.com/jessebot/onboardme/main/setup.sh

  # give it execute permissions
  chmod 0500 ./setup.sh
  ```

  ## run the setup.sh script
  This is to install dependencies and clone the onboardme repo.

  ```bash
  # NOTE THE . before the script! *Very* important!
  . ./setup.sh

  # just in case you didn't run the above script with .
  source ~/.bash_profile || source ~/.bashrc
  ```
  
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

  ```bash
  brew install python@3.10
  ```

</details>

### macOS
macOS uses zsh as the default shell, and I don't currently support zsh, so type
`bash` to get this ancient verison of bash to run the setup and and then
onboardme, which will install a current version of bash. **The script will *not* 
run properly in zsh**.

```bash
bash
```

## Actual installation

Recently, I started moving to actually package this, so you should be able to
do:
```bash
pip3.10 install onboardme
```

## Running `onboardme`
Now you can run the actual script that does the heavy lifting. If you ran the
above `setup.sh` and `pip install` without errors, you can start using
`onboardme` now:

```bash
# This will display a help
onboardme --help

# this will run the script with no options
onboardme
```

When the script completes, it'll output a number of other steps to take manually that aren't yet, or can't be, automated.

🎉 You're done! We're so proud of you. 🥹 _(and not in a sarcastic way, like we legitmately are proud of you for getting thorugh this awful alpha project doc)_
