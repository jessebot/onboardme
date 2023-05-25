# onbaordme Debian Bookworm image - for arm64 🤷
FROM debian:bookworm-slim

# ""        - will install onboardme and pre-reqs, but won't run it
# "default" - same as above, but runs: onboardme --no_upgrade --overwrite
ARG RUN_MODE=""

# this makes debian not prompt for stuff
ENV DEBIAN_FRONTEND=noninteractive

# install pre-req apt packages 
# python3 defaults to python 3.11 in Debian Bookworm
# added libreadline-dev because ruby suggested it
# added libyaml-dev, libncurses5-dev, libgdbm-dev, libffi-dev, and libreadline-dev because digital ocean guide said to
RUN apt-get update && \
    apt list --upgradeable | grep security | cut -f1 -d '/' | xargs apt-get install --no-install-recommends -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        file \
        git \
        python3-pip \
        python3-dev \
        openssh-client \
        libssl-dev \
        libreadline-dev \
        zlib1g-dev \
        autoconf \
        bison \
        sudo \
        libreadline-dev \
        libyaml-dev \
        libncurses5-dev \
        libffi-dev \
        libgdbm-dev

# create default user
RUN useradd -m friend && \
    usermod -aG sudo friend && \
    echo 'friend ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

WORKDIR /home/friend
USER friend

ENV HOME="/home/friend"

# make sure we can install executables locally 
ENV PATH="$PATH:$HOME/.local/bin:$HOME/.rbenv/bin:$HOME/.linuxbrew/bin:$PATH"

# homebrew on arm is weird. have to install ruby ourselves because of these err:
#0 2.005 Error: No Homebrew ruby 2.6.10_1 available for aarch64 processors!
#0 2.005 Error: Failed to install Homebrew Portable Ruby and cannot find another Ruby 2.6.10!
# see: https://github.com/orgs/Homebrew/discussions/3612
RUN curl -fsSL https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer | bash && \
    echo 'eval "$(rbenv init -)"' >> ~/.bashrc && \
    . ~/.bashrc && \
    rbenv install 2.6.10 && \
    rbenv global 2.6.10

# make python use our cache if the user wants to use XDG pathing
RUN if [ "$XDG" == "True" ]; then export PYTHONPYCACHEPREFIX=$XDG_CACHE_HOME/python; fi
# this isn't working via onboardme for some reason :(
# RUN if [ "$XDG" == "True" ]; then export PYTHONUSERBASE=$XDG_DATA_HOME/python; fi

# this is so that brew doesn't prompt for sudo access
ENV NONINTERACTIVE=1
# needed for linuxbrew, homebrew on Linux
ENV HOMEBREW_PREFIX="$HOME/.linuxbrew"
ENV HOMEBREW_CELLAR="$HOME/.linuxbrew/Cellar"
ENV HOMEBREW_REPOSITORY="$HOME/.linuxbrew/Homebrew"
ENV MANPATH="$MANPATH:$HOME/.linuxbrew/share/man"
ENV INFOPATH="$INFOPATH:$HOME/.linuxbrew/share/info"
ENV PATH="$PATH:$HOME/.linuxbrew/bin:$HOME/.linuxbrew/sbin"
ENV HOMEBREW_DEVELOPER=1
ENV HOMEBREW_USE_RUBY_FROM_PATH=1

RUN git clone https://github.com/Homebrew/brew.git ~/.linuxbrew && \
    eval "$(brew shellenv)" && \
    . /home/friend/.bashrc

# for standardizing where configs/state are installed
ENV XDG_CONFIG_HOME="$HOME/.config"
ENV XDG_CACHE_HOME="$HOME/.cache"
ENV XDG_DATA_HOME="$HOME/.local/share"
ENV XDG_STATE_HOME="$HOME/.local/state"

# this is for a cute fastfetch
COPY --chown=friend:friend docker_space_chalk /tmp/ff_config

# install onboardme - using python 3.11, default for Debian bookworm
# then run onboardme and clear apt/brew/pip cache when we're done
RUN pip install --user onboardme --break-system-packages && \
    onboardme --version && \
    if [ ! -z $RUN_MODE ]; then onboardme -O --no_upgrade -l debug && mv /tmp/ff_config ${XDG_CONFIG_HOME}/fastfetch/config.conf; fi && \
    brew cleanup && \
    sudo apt-get clean && \
    sudo pip cache purge && \
    sudo rm -rf /var/lib/apt/lists/* && \
    sudo rm -rf /tmp/*

ENTRYPOINT ["/bin/bash"]
