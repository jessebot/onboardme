#!/usr/bin/env bash
# just to install some quick reqs
# Checks for: Brew, git, python3, and python3 requirements.txt
# takes values of os you want to start, defaults to linux, but can do mac as well
os=$1

# git should be default installed on macOS Monterey, we but should check linux
which git
git_return_code=$?
if [ $git_return_code -ne 0 ]; then
    echo "Git not installed or in path, attempting to install git..."
    if [ "$os" == "debian" ]; then
        sudo apt install git
    fi
else
    echo "Git already installed :>"
fi

# check to make sure we have brew installed
which brew
brew_return_code=$?
if [ $brew_return_code -ne 0 ]; then
    echo "installing brew really quick, this will require your credentials for sudo abilities..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Brew is already installed :)"
fi


# check to make sure we have python installed
which python3
py_return_code=$?
if [ $py_return_code -ne 0 ]; then
    echo "We don't have python3 installed, installing..."
    brew install python3
else
    echo "Python3 is already installed :D"
fi


# I always put my projects in a directory called repos, idk why I can't stop...
echo "Creating directory structure..."
mkdir -p ~/repos && cd ~/repos

# Let's just download the repo now 
# haven't tested this: gh repo clone jessebot/onboardme
echo "Cloning the onboardme repo into ~/repos/onboardme ..."
git clone https://github.com/jessebot/onboardme.git


# make sure we have wget and pyyaml
echo "Now installing python reqs..."
pip install -r onboardme/requirements.txt

echo "Success~! You should be able to use onboardme.py now ^O^"
echo "Try running the following:"
echo "~/repos/onboardme/onboardme.py"
