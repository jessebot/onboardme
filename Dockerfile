# -- usage -- 
# docker run -it \
#   -v $(pwd):/onboardme \
#   onboardme \
#   /usr/bin/python3 -m build --wheel . && \
#   twine check dist/*

FROM ubuntu:latest as Base

ENV DEBIAN_FRONTEND=noninteractive
ENV HOMEBREW_PREFIX="/home/linuxbrew/.linuxbrew"
ENV HOMEBREW_CELLAR="/home/linuxbrew/.linuxbrew/Cellar"
ENV HOMEBREW_REPOSITORY="/home/linuxbrew/.linuxbrew/Homebrew"
ENV MANPATH="$MANPATH:/home/linuxbrew/.linuxbrew/share/man"
ENV INFOPATH="$INFOPATH:/home/linuxbrew/.linuxbrew/share/info"
ENV PATH="$PATH:/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin"
ENV NONINTERACTIVE=1
ENV PATH="$PATH:/home/onboardme/.local/bin"

WORKDIR /onboardme

# install apt packages and create user
RUN apt-get update && \
  apt-get upgrade -y && \
  useradd -ms /bin/bash onboardme && \
  apt-get install -y \
  python3-pip \
  python3-dev \
  python3.10-venv \
  wget \
  curl \
  git \
  vim && \
  apt-get install -y twine

RUN pip3.10 install wheel && \
  pip3.10 install build && \
  python3 -m pip install --upgrade build 

COPY . .

RUN python3 -m build --wheel . && \
  /usr/bin/twine check /onboardme/dist/* && \
  pip3.10 install -e . && \
  onboardme -O

# Install brew 
#RUN wget https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh && \
#  chmod +x /install.sh && \
#  chmod 777 /install.sh && \
#  /bin/bash install.sh
# git config --global init.defaultBranch main \
# Run setup.sh
#RUN wget https://raw.githubusercontent.com/jessebot/onboardme/main/setup.sh && \
#  chmod +x setup.sh && \
#  chmod 777 setup.sh && \
#  yes| /bin/bash setup.sh

