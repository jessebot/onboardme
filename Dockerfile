# onbaordme Debian Bookworm image
FROM debian:bookworm-slim

# ""        - will install onboardme, but won't run onboardme
# "default" - installs onboardme, and runs: onboardme --no_upgrade --overwrite
ARG RUN_MODE=""
ARG XDG="True"

# this makes debian not prompt for stuff
ENV DEBIAN_FRONTEND=noninteractive

# install pre-req apt packages 
# python3 defaults to python 3.11 in Debian Bookworm
RUN apt-get update && \
    apt list --upgradeable | grep security | cut -f1 -d '/' | xargs apt-get install --no-install-recommends -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    python3-pip \
    python3-dev \
    openssh-client \
    sudo \
    wget

# create default user
RUN useradd -m friend && \
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

# make python use our cache if the user wants to use XDG pathing
RUN if [ "$XDG" == "True" ]; then export PYTHONPYCACHEPREFIX=$XDG_CACHE_HOME/python && export PYTHONUSERBASE=$XDG_DATA_HOME/python; fi

# make sure we can install executables locally 
ENV PATH="$PATH:$HOME/.local/bin"

# this is so that brew doesn't prompt for sudo access
ENV NONINTERACTIVE=1
# needed for linuxbrew, homebrew on Linux
ENV HOMEBREW_PREFIX="/home/linuxbrew/.linuxbrew"
ENV HOMEBREW_CELLAR="/home/linuxbrew/.linuxbrew/Cellar"
ENV HOMEBREW_REPOSITORY="/home/linuxbrew/.linuxbrew/Homebrew"
ENV MANPATH="$MANPATH:/home/linuxbrew/.linuxbrew/share/man"
ENV INFOPATH="$INFOPATH:/home/linuxbrew/.linuxbrew/share/info"
ENV PATH="$PATH:/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin"
# installs brew and makes sure our default git branch is main
RUN wget https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh && \
   chmod +x install.sh && \
   chmod 777 install.sh && \
   /bin/bash install.sh && rm install.sh && \
   git config --global init.defaultBranch main

# install onboardme - using python 3.11, default for Debian bookworm
# then run onboardme and clear apt/brew/pip cache when we're done
RUN pip install --user onboardme --break-system-packages && \
    onboardme --version && \
    if [ ! -z $RUN_MODE ]; then onboardme -O --no_upgrade -l debug; fi && \
    brew cleanup && \
    sudo apt-get clean && \
    sudo rm -rf /var/lib/apt/lists/*

# not sure if this is breaking neovim from starting, might add back after testing
# pip cache purge && \
# sudo rm -rf /tmp/*

ENTRYPOINT ["/bin/bash"]
