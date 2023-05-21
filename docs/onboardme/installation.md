---
layout: default
title: Installation
grand_parent: onboardme
parent: Getting Started
permalink: /onboardme/getting-started/installation
---

# OnBoardMe Installation

### Prereq Installs
You'll need `curl`, `brew`, `git`, and Python 3.11 to get started. We have a setup script to install those (except `curl`) and help you get your environment to the XDG spec under <b>Locally</b> or you can just use our docker image, [jessebot/onboardme](https://hub.docker.com/r/jessebot/onboardme).

<details>
  <summary>Local prereq install script</summary>


<details>
  <summary><code>curl</code>, a pre-prereq</summary>

  ```bash
  # First, make sure you have curl, but it *should* be there already be on macOS.
  # if this doesn't return anything, you need to install curl
  which curl

  # Debian/Ubuntu may not have curl installed depending on where you are
  sudo apt install -y curl
  ```

  If it's not there on Linux, you can install it with `apt` or use any default package manager like yum, or whatever people who use gentoo use.

</details>

Make sure you have sudo access, otherwise we won't be able to install certain things.
The quickest way to get started on a fresh macOS or distro of Debian (including Ubuntu) is:
```bash
# this will download setup.sh to your current directory and run it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/jessebot/onboardme/main/setup.sh)"
```

#### Linux
Source your updated `.bashrc`:

```bash
# for linux
source ~/.bashrc
```

#### MacOS
source your updated `.bash_profile`:

```bash
bash
source ~/.bash_profile
```

You will still have to set your default shell to BASH to if you want to take advantage of the default dot files for onboardme. You can do that like this:

```bash
brew install bash
sudo -i

# if you're on an M1 or newer:
echo "/opt/homebrew/bin/bash" >> /etc/shells && exit
chsh -s /opt/homebrew/bin/bash $(whoami)

# if you're on a mac earlier than the M1:
echo "/usr/local/bin/bash" >> /etc/shells && exit
chsh -s /usr/local/bin/bash $(whoami)
```

After that, you can also set the shell directly in your terminal app via the settings.

If you finished the steps above, you can jump down to the [Actual installation](#actual-installation) section 😃

</details>


## Actual installation
You can install with `pip` still, but you can also use `pipx`.

<details>
  <summary><code>pip</code></summary>

```bash
# on Debian/Ubuntu you may have to also pass --break-system-packages
pip3.11 install --user --upgrade onboardme
```

</details>

<details>
  <summary><code>pipx</code></summary>

```bash
# untested
pipx install onboardme
```

</details>

## Using the Docker image

_Note: For fonts and images to work properly, you should use a modern terminal like [wezterm](https://wezfurlong.org/wezterm/), iterm2, or konsole as well as you need to make sure you [install](https://github.com/ryanoasis/nerd-fonts/tree/master#font-installation) a [nerdfont](https://www.nerdfonts.com) and_ `libsixel` + `imagemagick`.

To run the image locally with onboardme installed and already run using default settings:

```bash
# this image is built daily and has already run onboardme with the default settings
docker run jessebot/onboardme:latest
```

To run the image locally with onbaordme installed but _not_ run:

```bash
# best if you have your own dot files, or need a smaller initial docker image to pull
# no packages outside of the required pre-reqs for onboardme have been installed
docker run jessebot/onboardme:no-install
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

Now head over to the [Quickstart](https://jessebot.github.io/onboardme/onboardme/getting-started)
to get rolling!
