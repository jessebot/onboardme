#!/usr/bin/env bash
# just a quick script to install some reqs for onboardme
# works on Debian (Bookworm) based distros and macOS (13.0.1 and later)
# Checks for: brew, git, and python3.11

# extremely simply loading bar
function simple_loading_bar() {
    echo ""
    echo "          "
    for i in $(seq 1 $1); do
        echo -n "❤︎ ";
        sleep 1
    done
    echo ""
}

OS=$(uname)

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
        simple_loading_bar 5
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
if [ $git_return_code -eq 0 ]; then
    echo -e "\033[92mGit already installed :3 \033[00m"
else
    echo "Git not installed or in path, attempting to install git..."
    # we use *"linux"* because linux2 is a possibility, and who knows what else
    if [[ "$OS" == "Linux"* ]]; then
        sudo apt install git
        git_return_code=$?
        if [ $git_return_code -ne 0 ]; then
            echo "Git didn't install. This may be because you don't have main branch"
            echo "software enabled on Debian. You can enable that via the GUI under:"
            echo "Software & Updates (Software-properties-gtk) > Debian Software"
            exit
        fi
    fi
    # wait.... how can this work if brew doesn't work yet.... 🤔
    if [ "$OS" == "Darwin" ]; then
        echo "running: brew install git"
        brew install git
    fi
    echo -e "\033[92mGit Installed :3 \033[00m"
fi

echo "running: git config --global init.defaultBranch main"
git config --global init.defaultBranch main

# Make sure xcode is present on macOS, since it needs to be
# re-installed when upgrading from 12.x -> 13.x
if [ "$OS" == "Darwin" ]; then
    echo -e "-------------------------------- \033[94m Ensuring Xcode is present \033[00m ------------------------------"
    echo "running: xcode-select --install"
    xcode-select --install
fi


echo -e "------------------------------- \033[94m Checking for Brew \033[00m ------------------------------\n"

echo "Doing some linux brew path/env checking..."

# source the existing bashrc, just in case
if [ -f "~/.bashrc" ]; then
    . ~/.bashrc
elif [ -f "~/.bash_profile" ]; then
    . ~/.bash_profile
fi

env | grep -i "brew"
brew_return_code=$?

# if this still isn't in our path, export it and source this bashrc
if [ $brew_return_code -ne 0 ]; then
    if [[ "$OS" == *"Linux"* ]]; then
        echo "Linuxbrew isn't in your path. Let's get that installed :)"
        # make sure this is all in the bashrc for new shells
        echo "export HOMEBREW_PREFIX=/home/linuxbrew/.linuxbrew" >> ~/.bashrc
        echo "export HOMEBREW_CELLAR=/home/linuxbrew/.linuxbrew/Cellar" >> ~/.bashrc
        echo "export HOMEBREW_REPOSITORY=/home/linuxbrew/.linuxbrew/Homebrew" >> ~/.bashrc
        echo "export MANPATH=$MANPATH:/home/linuxbrew/.linuxbrew/share/man" >> ~/.bashrc
        echo "export INFOPATH=$INFOPATH:/home/linuxbrew/.linuxbrew/share/info" >> ~/.bashrc
        echo "PATH=$PATH:/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin" >> ~/.bashrc
        # source the bashrc, for this shell
        . ~/.bashrc
    else
        # check if this an M1 mac or not
        uname -a | grep arm > /dev/null
        M1=$?
        if [ $M1 -eq 0 ]; then
            # for the M1/M2 brew default installs here
            echo "PATH=/opt/homebrew/bin:$PATH" >> ~/.bash_profile
        fi
        # source the bashrc, for this shell
        . ~/.bash_profile
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
which python3.11 > /dev/null
py_return_code=$?
if [ $py_return_code -ne 0 ]; then
    echo "Installing Python3.11..."
    if [ "$OS" == "Darwin" ]; then
        brew install python@3.11
    else
        os_version=$(grep VERSION_CODENAME /etc/os-release | awk -F '=' '{print $2}')
        if [ $os_version == "bookworm" ]; then
            sudo apt install python3 python3-dev python3-pip
        else
            sudo apt install software-properties-common -y
            sudo add-apt-repository ppa:deadsnakes/ppa
            sudo apt install python3.11
            curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
        fi
    fi
    echo -e "\033[92mPython3.11 installed :3 \033[00m"
else
    echo -e "\033[92mPython3.11 already installed :3 \033[00m"
fi

echo -e "--------------------------\033[94m Installing OnBoardMe :D \033[00m -------------------------"

pip3.11 install onboardme
pip_install_return_code=$?

if [ $pip_install_return_code -ne 0 ]; then
    echo "Something went wrong with the installation of onboardme. :("
else
    echo ""
    echo -e "------------------------------ \033[92mSuccess~! ^O^\033[00m -----------------------------------"
    echo ""
    # source the existing bashrc, just in case
    if [[ "$OS" == *"Linux"* ]]; then
        echo -e "\033[92mPlease run:\033[00m source .bashrc"
    elif [ -f "~/.bash_profile" ]; then
        echo -e "\033[92mPlease run:\033[00m source .bash_profile"
    fi
    echo -e "✨ Then you can try running the following:"
    echo "onboardme --help"
    echo ""
fi
