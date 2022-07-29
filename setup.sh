#!/usr/bin/env bash
# just a quick script to install some reqs, works on debian based distros and macOS
# Checks for: Brew, git, python3, and python3 requirements.txt

# we make this lowercase because I don't trust it not to be random caps
OS=$(uname | tr '[:upper:]' '[:lower:]')

echo -e "-------------------------------- \033[94m 🛋️  Comfy Warning \033[00m -------------------------------"
echo "Before we begin, please make sure you're on a wired connection, or sitclose to the wifi. This "
echo "might take a while if you're a fresh OS install and you'll need to present to enter your password "
echo "for package installs, so grab some tea and get comfy :3"
printf "\nHere's some relaxing music: https://youtu.be/-5KAN9_CzSA"
while true; do
    printf "\n\n"
    read -p "Are you ready to get started? Do you have a nice cup of ☕? [y/n] " answer
    if [ "$answer" != "y" ]; then
        printf "\nThat's totally reasonable. You take your time, and I will be here."
        sleep 5
    else
        break
    fi
done

echo -e "\n-------------------------------- \033[94m 🎬 Beginning Setup \033[00m -------------------------------"
echo ""
if [[ "$OS" == *"Linux"* ]]; then
    echo -e "---------------------------- \033[94m Updating existing apt packages \033[00m --------------------"
    sudo apt update && sudo apt upgrade
    echo -e "\033[92m apt updated/upgraded :3 \033[00m"
fi

# git should be default installed on macOS Monterey :shrug:
echo -e "-------------------------------- \033[94m Checking for Git \033[00m ------------------------------"
which git > /dev/null
git_return_code=$?
if [ $git_return_code -ne 0 ]; then
    echo "Git not installed or in path, attempting to install git..."
    # we use *"Linux"* because linux2 is a possibility, and who knows what else
    if [[ "$OS" == *"Linux"* ]]; then
        sudo apt install git
        git_return_code=$?
        if [ $git_return_code -ne 0 ]; then
            echo "Git didn't install. This may be because you don't have main branch"
            echo "software enabled on Debian. You can enable that via the GUI under:"
            echo "Software & Updates (Software-properties-gtk) > Debian Software"
            exit
        fi
    fi
    if [ "$OS" == "darwin" ]; then
        brew install git
    fi
    echo -e "\033[92mGit Installed :3 \033[00m"
else
    echo -e "\033[92mGit already installed :3 \033[00m"
fi


echo -e "------------------------------- \033[94m Checking for Brew \033[00m ------------------------------"
# make sure linuxbrew is in the path
if [[ "$OS" == *"Linux"* ]]; then
    # source the existing bashrc, just in case
    if [ -f "~/.bashrc" ]; then
        source ~/.bashrc
    fi

    # if this still isn't in our path, export it and source this bashrc
    if [[ "linuxbrew" != *"$PATH"* ]]; then
        echo "Linuxbrew isn't in your path. Let's get that installed :)"
        echo 'HOMEBREW_PREFIX="/home/linuxbrew/.linuxbrew"' >> ~/.bashrc
        echo 'HOMEBREW_CELLAR="/home/linuxbrew/.linuxbrew/Cellar"' >> ~/.bashrc
        echo 'HOMEBREW_REPOSITORY="/home/linuxbrew/.linuxbrew/Homebrew"' >> ~/.bashrc
        echo 'PATH="/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin${PATH+:$PATH}"' >> ~/.bashrc
        echo 'MANPATH="/home/linuxbrew/.linuxbrew/share/man${MANPATH+:$MANPATH}:"' >> ~/.bashrc
        echo 'INFOPATH="/home/linuxbrew/.linuxbrew/share/info${INFOPATH:-}"' >> ~/.bashrc
        source ~/.bashrc
    fi
fi

which brew > /dev/null
brew_return_code=$?
if [ $brew_return_code -ne 0 ]; then
    echo "Installing brew really quick, this will require your credentials for sudo abilities..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo -e "\033[92mBrew installed :3 \033[00m"
else
    echo -e "\033[92mBrew already installed :3 \033[00m"
fi


echo -e "--------------------------\033[94m Checking for Python3 and pip3\033[00m -------------------------"
# check to make sure we have python3 and pip3 installed
which python3 > /dev/null
py_return_code=$?
if [ $py_return_code -ne 0 ]; then
    echo "Installing Python3..."
    brew install python3
    echo -e "\033[92mPython installed :3 \033[00m"
else
    echo -e "\033[92mPython already installed :3 \033[00m"
fi

which pip3 > /dev/null
pip_return_code=$?
if [ $pip_return_code -ne 0 ]; then
    echo "Installing Pip3..." 
    if [[ "$OS" == *"Linux"* ]]; then
        sudo apt install python3-pip
        echo -e "\033[92mPip3 installed :3 \033[00m"
    fi
else
    echo -e "\033[92mPip3 already installed :3 \033[00m"
fi

# I always put my projects in a directory called repos, idk why I can't stop...
echo -e "--------------------- \033[94mCreating directories and cloning repo...\033[00m ---------------------"
mkdir -p ~/repos
git clone https://github.com/jessebot/onboardme.git ~/repos/onboardme

# we do this for Debian, to download custom fonts during onboardme
if [[ "$OS" == *"Linux"* ]]; then
    mkdir -p ~/.local/share/fonts
fi

# make sure we have wget and pyyaml
echo "Now installing python reqs..."
pip3 install -r ~/repos/onboardme/requirements.txt 
echo ""
echo -e "------------------------------ \033[92mSuccess~! ^O^\033[00m -----------------------------------"
echo ""
echo -e "✨ Now, try running the following: ~/repos/onboardme/onboardme.py --help"
echo ""
