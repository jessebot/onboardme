#!/usr/bin/env bash
# just a quick script to install some reqs, works on debian based distros and macOS
# Checks for: Brew, git, python3, and python3 requirements.txt

# we make this lowercase because I don't trust it not to be random caps
OS=$(uname | tr '[:upper:]' '[:lower:]')

echo "This script will ask for your password to sudo install things"

echo -e "-------------------------------- \033[00m Beginning Setup \033[00m -------------------------------"
echo "Before we begin, please make sure you're on a wired connection,"
echo "or sitting close to the wifi."

if [[ "$OS" == *"linux"* ]]; then
    echo -e "---------------------------- \033[00m Updating existing apt packages \033[00m --------------------"
    sudo apt update && sudo apt upgrade
    echo -e "\033[92m apt updated/upgraded :3 \033[92m"
fi

# git should be default installed on macOS Monterey :shrug:
echo -e "-------------------------------- \033[00m Checking for Git \033[00m ------------------------------"
which git > /dev/null
git_return_code=$?
if [ $git_return_code -ne 0 ]; then
    echo "Git not installed or in path, attempting to install git..."
    # we use *"linux"* because linux2 is a possibility, and who knows what else
    if [[ "$OS" == *"linux"* ]]; then
        sudo apt install git
    fi
    if [ "$OS" == "darwin" ]; then
        brew install git
    fi
    echo -e "\033[92m Git Installed :3 \033[92m"
else
    echo -e "\033[92mGit already installed :3 \033[92m"
fi
echo "--------------------------------------------------------------------------------"

# make sure linuxbrew is in the path
if [[ "$OS" == *"linux"* ]]; then
    export PATH=$PATH:/home/linuxbrew/.linuxbrew/bin
fi

# check to make sure we have brew installed
which brew > /dev/null
brew_return_code=$?
if [ $brew_return_code -ne 0 ]; then
    echo "Installing brew really quick, this will require your credentials for sudo abilities..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo -e "\033[92mBrew installed :3 \033[92m"
else
    echo -e "\033[92mBrew already installed :3 \033[92m"
fi
echo "--------------------------------------------------------------------------------"


# check to make sure we have python3 and pip3 installed
which python3 > /dev/null
py_return_code=$?
if [ $py_return_code -ne 0 ]; then
    echo "Installing Python3..."
    brew install python3
    echo -e "\033[92mPython installed :3 \033[92m"
else
    echo -e "\033[92mPython already installed :3 \033[92m"
fi
echo "--------------------------------------------------------------------------------"

which pip3
pip_return_code=$?
if [ $pip_return_code -ne 0 ]; then
    echo "Installing Pip3..." 
    if [[ "$OS" == *"linux"* ]]; then
        sudo apt install python3-pip
        echo -e "\033[92mPip3 installed :3 \033[92m"
    fi
else
    echo -e "\033[92mPip3 already installed :3 \033[92m"
fi
echo "--------------------------------------------------------------------------------"


# I always put my projects in a directory called repos, idk why I can't stop...
echo -e "----------------------\033[00mCreating directory and cloning repo...\033[00m----------------------"
mkdir -p ~/repos && git clone https://github.com/jessebot/onboardme.git ~/repos/onboardme

# Let's just download the repo now 
echo "Cloning the onboardme repo into ~/repos/onboardme ..."
echo "--------------------------------------------------------------------------------"


# make sure we have wget and pyyaml
echo "Now installing python reqs..."
pip3 install -r ~/repos/onboardme/requirements.txt 
echo ""
echo "------------------------------ Success~! ^O^ -----------------------------------"
echo ""
echo "Now, try running the following: ~/repos/onboardme/onboardme.py"
echo ""
