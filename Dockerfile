# onbaordme testing Debian Bookworm image
# -- usage --
# docker build . -t onboardme:dev
# docker run -it onboardme:dev /bin/bash
FROM debian:bookworm-slim

# this makes debian not prompt for stuff
ENV DEBIAN_FRONTEND=noninteractive

# this is so that brew doesn't prompt for sudo access
ENV NONINTERACTIVE=1

# install pre-req apt packages
RUN apt-get update && \
  apt list --upgradeable | grep security | cut -f1 -d '/' | xargs apt install --no-install-recommends -y && \
  apt-get install -y --no-install-recommends \
  build-essential \
  curl \
  git \
  python3-pip \
  python3-dev \
  python3-venv \
  openssh-client \
  sudo \
  wget

# create default user
RUN useradd -ms /usr/sbin/nologin friend && \
    usermod -aG sudo friend && \
    echo 'friend ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

WORKDIR /home/friend
USER friend

# for standardizing where configs/state are installed
ENV HOME="/home/friend"
ENV XDG_CONFIG_HOME="$HOME/.config"
ENV XDG_CACHE_HOME="$HOME/.cache"
ENV XDG_DATA_HOME="$HOME/.local/share"
ENV XDG_STATE_HOME="$HOME/.local/state"

# make sure we can install executables locally 
ENV PATH="$PATH:$HOME/.local/bin"

# needed for Homebrew on Linux
ENV HOMEBREW_PREFIX="/home/linuxbrew/.linuxbrew"
ENV HOMEBREW_CELLAR="/home/linuxbrew/.linuxbrew/Cellar"
ENV HOMEBREW_REPOSITORY="/home/linuxbrew/.linuxbrew/Homebrew"
ENV MANPATH="$MANPATH:/home/linuxbrew/.linuxbrew/share/man"
ENV INFOPATH="$INFOPATH:/home/linuxbrew/.linuxbrew/share/info"
ENV PATH="$PATH:/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin"

# installs brew
RUN wget https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh && \
    chmod +x ./install.sh && \
    ./install.sh && \
    rm install.sh

# makes sure our default branch is main
RUN git config --global init.defaultBranch main

# installs onboardme from pypi - using python 3.11, default for Debian bookworm
# and run onboardme at the end
RUN pip install --user onboardme --break-system-packages && \
    onboardme --version

# Options: ""     - will not install anything with onboardme
#          "default" - default installation mode - only install cli packages
ARG RUN_MODE=""
RUN if [ ! -z $RUN_MODE ]; then onboardme -O; fi

RUN brew cleanup && \
    sudo apt-get clean && \
    sudo rm -rf /var/lib/apt/lists/* && \
    sudo rm -rf /tmp
