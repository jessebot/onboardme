#!/usr/bin/env bash
# just to install some quick reqs

# check to make sure we have brew installed
which brew
brew_return_code=$?
if [ $brew_return_code -ne 0 ]; then
    echo "installing brew really quick..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# check to make sure we have python installed
which python3
py_return_code=$?
if [ $py_return_code -ne 0 ]; then
    echo "We don't have python3 installed, installing..."
    brew install python3
fi

# make sure we have wget and pyyaml :D
echo "Now installing python reqs"
pip install -r requirements.txt

# success!
echo "You should be able to use onboardme.py now :)"
