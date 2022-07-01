#!/usr/bin/env bash
# just a quick script to install some reqs, works on debian based distros and macOS
# Checks for: Brew, git, python3, and python3 requirements.txt

# we make this lowercase because I don't trust it not to be random caps
OS=$(uname | tr '[:upper:]' '[:lower:]')

echo "This script will ask for your password to sudo install things."

echo "-------------------------------- Beginning Setup -------------------------------"
# git should be default installed on macOS Monterey, we but should check linux
which git > /dev/null
git_return_code=$?
if [ $git_return_code -ne 0 ]; then
    echo "Git not installed or in path, attempting to install git..."
    # we use *"linux"* because linux2 is a possibility, and who knows what else
    if [[ "$OS" == *"linux"* ]]; then
        sudo apt install git
    fi
else
    echo "Git already installed :>"
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
else
    echo "Brew is already installed :)"
fi
echo "--------------------------------------------------------------------------------"


# check to make sure we have python3 and pip3 installed
which python3 > /dev/null
py_return_code=$?
if [ $py_return_code -ne 0 ]; then
    echo "Installing Python3..."
    brew install python3
else
    echo "Python3 is already installed :D"
fi
echo "--------------------------------------------------------------------------------"

which pip3
pip_return_code=$?
if [ $pip_return_code -ne 0 ]; then
    echo "Installing Pip3..." 
    if [[ "$OS" == *"linux"* ]]; then
        sudo apt install python3-pip
    fi
else
    echo "Pip3 is already installed as well :D"
fi
echo "--------------------------------------------------------------------------------"


# I always put my projects in a directory called repos, idk why I can't stop...
echo "Creating directory structure..."
mkdir -p ~/repos
echo "--------------------------------------------------------------------------------"

# Let's just download the repo now 
# haven't tested this: gh repo clone jessebot/onboardme
echo "Cloning the onboardme repo into ~/repos/onboardme ..."
git clone https://github.com/jessebot/onboardme.git ~/repos/onboardme
echo "--------------------------------------------------------------------------------"


# make sure we have wget and pyyaml
echo "Now installing python reqs..."
pip3 install -r ~/repos/onboardme/requirements.txt 
echo ""
echo "------------------------------ Success~! ^O^ -----------------------------------"
echo ""
echo "Now, try running the following:"
echo "cd ~/repos/onboardme/onboardme.py && ./onboardme.py"
echo ""
