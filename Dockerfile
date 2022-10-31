FROM ubuntu:latest as Base

ENV DEBIAN_FRONTEND=noninteractive
ENV HOMEBREW_PREFIX="/home/linuxbrew/.linuxbrew"
ENV HOMEBREW_CELLAR="/home/linuxbrew/.linuxbrew/Cellar"
ENV HOMEBREW_REPOSITORY="/home/linuxbrew/.linuxbrew/Homebrew"
ENV MANPATH="$MANPATH:/home/linuxbrew/.linuxbrew/share/man"
ENV INFOPATH="$INFOPATH:/home/linuxbrew/.linuxbrew/share/info"
ENV PATH="$PATH:/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin"
ENV NONINTERACTIVE=1
ENV PATH="$PATH:/root/.local/bin"

# install apt packages and create user
RUN apt-get update && \
  apt-get upgrade -y && \
  useradd -ms /bin/bash onboardme && \
  apt-get install -y python3-pip python3-dev wget curl git vim && \
  git config --global init.defaultBranch main 

# Install brew 
RUN wget https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh && \
  chmod +x /install.sh && \
  chmod 777 /install.sh && \
  /bin/bash install.sh

# Run setup.sh
RUN wget https://raw.githubusercontent.com/jessebot/onboardme/main/setup.sh && \
  chmod +x setup.sh && \
  chmod 777 setup.sh && \
  yes| /bin/bash setup.sh


