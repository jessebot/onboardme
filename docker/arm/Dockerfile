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
    libgdbm-dev \
    wget

# create default user
RUN useradd -m friend && \
    usermod -aG sudo friend && \
    echo 'friend ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

WORKDIR /home/friend
USER friend

# this is so that brew doesn't prompt for sudo access, not sure if relevant on arm
ENV NONINTERACTIVE=1

# make sure we can install executables locally 
ENV PATH="/home/friend/.rbenv/bin:home/friend/.linuxbrew/bin:$PATH"

# homebrew on arm is weird. have to install ruby ourselves because of these err:
#0 2.005 Error: No Homebrew ruby 2.6.10_1 available for aarch64 processors!
#0 2.005 Error: Failed to install Homebrew Portable Ruby and cannot find another Ruby 2.6.10!
# see: https://github.com/orgs/Homebrew/discussions/3612
RUN curl -fsSL https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer | bash && \
    echo 'eval "$(rbenv init -)"' >> ~/.bashrc && \
    . ~/.bashrc && \
    rbenv install 2.6.10 && \
    rbenv global 2.6.10

ENV HOMEBREW_DEVELOPER=1
ENV HOMEBREW_USE_RUBY_FROM_PATH=1
RUN git clone https://github.com/Homebrew/brew.git .linuxbrew && \
    eval "$(brew shellenv)" && \
    . /home/friend/.bashrc
RUN brew update

ENTRYPOINT ["/bin/bash"]
