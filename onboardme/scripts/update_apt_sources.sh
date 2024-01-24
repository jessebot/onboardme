#!/usr/bin/env bash
# OS_VERSION=$1
OS_VERSION="12"

# enables contribution and non-free apt package manager sources
# append "contrib non-free" to lines that end with "bookworm main"
sed -i 's/bookworm main$/bookworm main contrib non-free/g' /etc/apt/sources.list


# add lutris repos
# see: https://software.opensuse.org/download.html?project=home%3Astrycore&package=lutris
# also see: https://lutris.net/downloads
echo "deb [signed-by=/etc/apt/keyrings/lutris.gpg] https://download.opensuse.org/repositories/home:/strycore/$OS_VERSION/ ./" | sudo tee /etc/apt/sources.list.d/lutris.list > /dev/null
wget -q -O- https://download.opensuse.org/repositories/home:/strycore/Debian_$OS_VERSION/Release.key | gpg --dearmor | sudo tee /etc/apt/keyrings/lutris.gpg > /dev/null
sudo apt update
