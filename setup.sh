#!/usr/bin/env bash
# just a quick script to install some reqs, works on debian based distros and macOS
# Checks for: Brew, git, python3, and python3 requirements.txt

# git should be default installed on macOS Monterey, we but should check linux
which git > /dev/null
git_return_code=$?
if [ $git_return_code -ne 0 ]; then
    printf "Git not installed or in path, attempting to install git...\n\n"
    if [ $(uname) == "linux" ]; then
        sudo apt install git
    fi
else
    printf "Git already installed :>\n\n"
fi

# check to make sure we have brew installed
which brew > /dev/null
brew_return_code=$?
if [ $brew_return_code -ne 0 ]; then
    printf "installing brew really quick, this will require your credentials for sudo abilities...\n\n"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    printf "Brew is already installed :)\n\n"
fi


# check to make sure we have python installed
which python3 > /dev/null
py_return_code=$?
if [ $py_return_code -ne 0 ]; then
    printf "We don't have python3 installed, installing...\n\n"
    brew install python3
else
    printf "Python3 is already installed :D\n\n"
fi


# I always put my projects in a directory called repos, idk why I can't stop...
printf "Creating directory structure...\n\n"
mkdir -p ~/repos

# Let's just download the repo now 
# haven't tested this: gh repo clone jessebot/onboardme
printf "Cloning the onboardme repo into ~/repos/onboardme ...\n\n"
git clone https://github.com/jessebot/onboardme.git ~/repos/onboardme


# make sure we have wget and pyyaml
printf "Now installing python reqs...\n\n"
pip install -r ~/repos/onboardme/requirements.txt

printf "Success~! You should be able to use onboardme.py now ^O^\n\n"
printf "Try running the following:\n"
printf "~/repos/onboardme/onboardme.py\n\n"
