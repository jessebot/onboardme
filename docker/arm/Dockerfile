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
    libreadline-dev \
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
ENV PATH="/home/friend/.rbenv/bin:$PATH:/opt/Homebrew/bin"

# homebrew on arm is weird. have to install ruby ourselves because of these err:
#0 2.005 Error: No Homebrew ruby 2.6.10_1 available for aarch64 processors!
#0 2.005 Error: Failed to install Homebrew Portable Ruby and cannot find another Ruby 2.6.10!
# see: https://github.com/orgs/Homebrew/discussions/3612
RUN git clone https://github.com/rbenv/rbenv.git /home/friend/.rbenv && \
    chmod +x /home/friend/.rbenv/bin/rbenv && \
    echo 'eval "$(/home/friend/.rbenv/bin/rbenv init - bash)"' >> /home/friend/.bashrc && \
    eval "$(/home/friend/.rbenv/bin/rbenv init - bash)" && \
    git clone https://github.com/rbenv/ruby-build.git "$(rbenv root)"/plugins/ruby-build

RUN echo "made it here :P"

# https://github.com/Homebrew/brew/blob/8aaf99e1d70c5f50a828c34c3219ecfb17203ba0/Library/Homebrew/Gemfile#L6
# - - - - - - - - - - - - - - - - - - -
# if ENV.fetch("HOMEBREW_DEVELOPER", "").empty? || ENV.fetch("HOMEBREW_USE_RUBY_FROM_PATH", "").empty?
#   ruby "~> 2.6.0"
# else
#   ruby ">= 2.6.0"
# end
# - - - - - - - - - - - - - - - - - - -
# Homebrew actually errors about 2.6.10, but we'll try with this instead,
# because it looks like ~> should mean greater than 2.6.0 for patch versions only?
RUN rbenv install 2.6.10

# homebrew on arm is weird. see: https://github.com/orgs/Homebrew/discussions/3612
RUN sudo mkdir -p /opt/Homebrew && \
    sudo chmod 777 /opt/Homebrew && \
    sudo chown friend: /opt/Homebrew && \
    git clone https://github.com/Homebrew/brew.git /opt/Homebrew && \
    export PATH="$HOME/.rbenv/shims:$PATH"

# check that ruby is correct version
# RUN $(which ruby) --enable-frozen-string-literal --disable=gems,did_you_mean,rubyopt $(/opt/Homebrew/bin/brew --prefix)/Homebrew/Library/Homebrew/utils/ruby_check_version_script.rb 2.6.10 && echo "ruby is here and OK"

RUN . /home/friend/.bashrc

# this is to reload the shell
# USER root
# USER friend

ENV HOMEBREW_DEVELOPER=1
ENV HOMEBREW_USE_RUBY_FROM_PATH=1
# RUN brew update

ENTRYPOINT ["/bin/bash"]
