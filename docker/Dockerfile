# onbaordme Debian Bookworm image - linux/amd64 only
FROM debian:bookworm-slim

# ""           - will install onboardme, but won't run onboardme
# "default"    - onboardme --no_upgrade
ARG RUN_MODE=""
# onboardme --no_upgrade -s packages -g devops
ARG DEVOPS=""
# onboardme --no_upgrade -s packages -g music
ARG MUSIC=""
# onboardme --no_upgrade -s packages -g mail
ARG MAIL=""
# onboardme --no_upgrade -s packages -g data_science
ARG DATA_SCIENCE=""

# makes debian not prompt for stuff
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
RUN export PYTHONPYCACHEPREFIX=$XDG_CACHE_HOME/python
# this isn't working via onboardme for some reason :(
# RUN export PYTHONUSERBASE=$XDG_DATA_HOME/python

# make sure we can install executables locally 
ENV PATH="$PATH:$HOME/.local/bin"

# so that brew doesn't prompt for sudo access
ENV NONINTERACTIVE=1
# needed for linuxbrew, homebrew on Linux
ENV HOMEBREW_PREFIX="/home/linuxbrew/.linuxbrew"
ENV HOMEBREW_CELLAR="/home/linuxbrew/.linuxbrew/Cellar"
ENV HOMEBREW_REPOSITORY="/home/linuxbrew/.linuxbrew/Homebrew"
ENV MANPATH="$MANPATH:/home/linuxbrew/.linuxbrew/share/man"
ENV INFOPATH="$INFOPATH:/home/linuxbrew/.linuxbrew/share/info"
ENV PATH="$PATH:/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin"

# installs brew, sets default git branch to main, and moves gitconfig to /home/.config/git/config
RUN wget --hsts-file="$XDG_DATA_HOME/wget/wget-hsts" https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh && \
    chmod +x install.sh && \
    chmod 777 install.sh && \
    /bin/bash install.sh && rm install.sh && \
    git config --global init.defaultBranch main && \
    mkdir -p $XDG_CONFIG_HOME/git && \
    mv $HOME/.gitconfig $XDG_CONFIG_HOME/git/config

# this is for a cute fastfetch
COPY --chown=friend:friend config.conf /tmp/

# install onboardme - using python 3.11, default for Debian bookworm
# then run onboardme and clear apt/brew/pip cache when we're done
RUN pip install --user onboardme --break-system-packages && \
    onboardme --version && \
    if [ ! -z $RUN_MODE ]; then \
      onboardme -O --no_upgrade -l debug && \
      mv /tmp/config.conf ${XDG_CONFIG_HOME}/fastfetch/config.conf; fi

RUN if [ -n $DEVOPS ]; then onboardme -O --no_upgrade -l debug -s packages -g devops && bash /tmp/devops-onboardme-install.sh; fi && \
    if [ -n $MUSIC ]; then onboardme -O --no_upgrade -l debug -s packages -g music && bash /tmp/music-onboardme-install.sh; fi && \
    if [ -n $MAIL ]; then  onboardme -O --no_upgrade -l debug -s packages -g mail; fi && \
    if [ -n $DATA_SCIENCE ]; then onboardme -O --no_upgrade -l debug -s packages -g data_science; fi

RUN brew cleanup && \
    sudo apt-get clean && \
    sudo pip cache purge && \
    sudo rm -rf /var/lib/apt/lists/* && \
    sudo rm -rf /tmp/*

ENTRYPOINT ["/bin/bash"]
