# onbaordme Debian Bookworm image - for arm64 🤷
FROM debian:bookworm-slim

# ""        - will install onboardme and pre-reqs, but won't run it
# "default" - same as above, but runs: onboardme --no_upgrade --overwrite
ARG RUN_MODE=""

# this makes debian not prompt for stuff
ENV DEBIAN_FRONTEND=NONINTERACTIVE

# install pre-req apt packages 
# python3 defaults to python 3.11 in Debian Bookworm
RUN apt-get update && \
    apt list --upgradeable | grep security | cut -f1 -d '/' | xargs apt-get install --no-install-recommends -y && \
    apt-get install -y \
        build-essential \
        curl \
        file \
        procps \
        git \
        python3-pip \
        python3-dev \
        openssh-client \
        sudo \
        autoconf \
        bison \
        patch \
        libssl-dev \
        libyaml-dev \
        libreadline-dev \
        zlib1g-dev \
        libgmp-dev \
        libncurses5-dev \
        libffi-dev \
        libgdbm6 \
        libgdbm-dev \
        libdb-dev \
        uuid-dev

# create default user
RUN useradd -m friend && \
    usermod -aG sudo friend && \
    echo 'friend ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

WORKDIR /home/friend
USER friend

ENV HOME="/home/friend"

# make sure we can run locally installed executables
ENV PATH="$HOME/.rbenv/bin:/home/linuxbrew/.linuxbrew/bin:$HOME/.local/bin:$PATH"

# ref: https://github.com/rbenv/rbenv-installer
# installs rbenv, ruby-build, followed by openssl 1.1 and finally ruby 2.6.10
# takes 25-45 min to compile stuff unless docker has like 8 CPU/16G mem in resources
RUN curl -fsSL https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer | bash && \
    eval "$(rbenv init -)" && \
    . $HOME/.bashrc && \
    rbenv install 2.6.10 && \
    rbenv global 2.6.10 && \
    sudo ln -s $HOME/.rbenv/versions/2.6.10/bin/ruby /usr/bin/ruby

# this is so that brew doesn't prompt for sudo access
ENV NONINTERACTIVE=1

# suggestion by homebrew member:
# https://github.com/orgs/Homebrew/discussions/3612#discussioncomment-3572967
ENV HOMEBREW_DEVELOPER=1
ENV HOMEBREW_USE_RUBY_FROM_PATH=1

# homebrew on arm is unsupported: https://docs.brew.sh/Homebrew-on-Linux#arm-unsupported
# so we have to install ruby ourselves because of:
# Error: No Homebrew ruby 2.6.10_1 available for aarch64 processors!
# Error: Failed to install Homebrew Portable Ruby and cannot find another Ruby 2.6.10!
# see: https://github.com/orgs/Homebrew/discussions/3612
RUN sudo mkdir /home/linuxbrew && sudo chmod 755 /home/linuxbrew && sudo chown friend: /home/linuxbrew && \
    git clone https://github.com/Homebrew/brew.git /home/linuxbrew/.linuxbrew && \
    eval "$(brew shellenv)" && \
    echo 'eval "$(brew shellenv)"' >> ${HOME}/.bashrc && \
    . $HOME/.bashrc

# for standardizing where configs/state are installed
ENV XDG_CONFIG_HOME="$HOME/.config"
ENV XDG_CACHE_HOME="$HOME/.cache"
ENV XDG_DATA_HOME="$HOME/.local/share"
ENV XDG_STATE_HOME="$HOME/.local/state"

# make python use our cache if the user wants to use XDG pathing
RUN if [ "$XDG" == "True" ]; then export PYTHONPYCACHEPREFIX=$XDG_CACHE_HOME/python; fi

# this isn't working via onboardme for some reason :(
RUN if [ "$XDG" == "True" ]; then export PYTHONUSERBASE=$XDG_DATA_HOME/python; fi

# install onboardme - using python 3.11, default for Debian bookworm
# then run onboardme and clear apt/brew/pip cache when we're done
RUN pip install --user onboardme --break-system-packages

RUN onboardme --version

# this is for a cute fastfetch
COPY --chown=friend:friend docker_space_chalk /tmp/ff_config

RUN if [ ! -z $RUN_MODE ]; then onboardme -O --no_upgrade -l debug && mv /tmp/ff_config ${XDG_CONFIG_HOME}/fastfetch/config.conf; fi && \
    brew cleanup && \
    sudo apt-get clean && \
    sudo pip cache purge && \
    sudo rm -rf /var/lib/apt/lists/* && \
    sudo rm -rf /tmp/*

ENTRYPOINT ["/bin/bash"]
