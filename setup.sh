#!/usr/bin/env bash
# just a quick script to install some reqs, works on debian based distros and macOS
# Checks for: Brew, git, python3, and python3 requirements.txt
OS=`$(uname) | tr '[:upper:]' '[:lower:]'`

echo "-------------------------------- Beginning Setup -------------------------------"
# git should be default installed on macOS Monterey, we but should check linux
which git > /dev/null
git_return_code=$?
if [ $git_return_code -ne 0 ]; then
    echo "Git not installed or in path, attempting to install git..."
    if [ "$OS" == "linux" ]; then
        sudo apt install git
    fi
else
    echo "Git already installed :>"
fi
echo "--------------------------------------------------------------------------------"

# make sure linuxbrew is in the path
if [ "$OS" == "linux" ]; then
    export PATH=$PATH:/home/linuxbrew/.linuxbrew/bin
    echo "path is: $PATH"
    PATH=$PATH:/home/linuxbrew/.linuxbrew/bin
    echo "path is: $PATH"
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


# check to make sure we have python installed
which python3 > /dev/null
py_return_code=$?
if [ $py_return_code -ne 0 ]; then
    echo "Installing Python3..."
    brew install python3
else
    echo "Python3 is already installed :D"
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
pip install -r ~/repos/onboardme/requirements.txt 
echo ""
echo "------------------------------ Success~! ^O^ -----------------------------------"
echo ""
echo "Now, try running the following: ~/repos/onboardme/onboardme.py"
echo ""
