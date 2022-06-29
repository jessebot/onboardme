#!/usr/bin/env python3
# Generic onboarding script for mac osx and debian
# jessebot@linux.com
import argparse
import os
import subprocess
import sys
from sys import platform
import yaml

HOME_DIR = os.getenv("HOME")
OS = platform
CONFIG_FILE = yaml("packages/packages.yaml")


def run_apt_installs():
    """
    install every apt package in packages.yaml
    """
    for package in CONFIG_FILE["apt_packages"]:
        apt_install_cmd = f"apt install {package}"
        result = subproc(apt_install_cmd)

    return None


def run_brew_installs():
    """
    brew install from the brewfiles
    """
    # make sure brew is installed
    url = "https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh"
    install_cmd = f'/bin/bash -c "$(curl -fsSL {url})"'
    result = subproc(install_cmd)

    # this is the stuff that's installed on both mac and linux
    brew_cmd = "brew bundle --file=./packages/Brewfile_standard"
    result = subproc(brew_cmd)

    # install linux specific apps
    if OS == 'linux' or OS == 'linux2':
        brew_cmd = "brew bundle --file=./packages/Brewfile_linux"
        result = subproc(brew_cmd)
    # install mac specific apps
    elif OS == 'darwin':
        brew_cmd = "brew bundle --file=./packages/Brewfile_mac"
        result = subproc(brew_cmd)

    return None


def run_upgrades():
    """
    run upgrade and update for every package manager
    """
    apt_update_upgrade_cmd = f"apt upgrade && apt update"
    result = subproc(apt_update_upgrade_cmd)

    brew_update_upgrade_cmd = f"brew upgrade && brew update"
    result = subproc(brew_update_upgrade_cmd)


def install_rc_files():
    """
    Copies over default rc files for vim, zsh, and bash
    """
    rc_files = ['vim','zsh','bash']
    vim_plugin_manager = ("git clone "
                          "https://github.com/VundleVim/Vundle.vim.git"
                          "~/.vim/bundle/Vundle.vim")
    for rc_file in rc_files:
        shutil.copytree('configs/rc_files/{rc_file}/', HOME_DIR)
    return None


def configure_firefox():
    """
    Copies over default firefox settings and addons 
    """
    shutil.copy('configs/browser/firefox/user.js', FIREFOX_PROFILE_DIR)

    shutil.copytree('configs/browser/firefox/distribution/extensions/',
                    FIREFOX_EXT_DIR)

    print("Copied over firefox settings")
    return None


def subproc(cmd, help="Something went wrong!"):
    """
    Takes a commmand to run in BASH, as well as optional
    help text, both str
    """
    print("Running command: {cmd}")
    command = cmd.split()
    res_err = ""
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        return_code = p.returncode
        res_out = p.communicate()
        # check return code, raise error if failure
        if return_code != 0:
            err = "Return code was not zero! It was:" + \
                  " {0} see res: ".format(return_code)
            raise Exception(err)
    except Exception as e:
        if res_err:
            print("ERROR: " + " ".join([help, e, res_out]))

    return res_out


def main():
    """
    Core function
    """
    help = 'This is a generic onboarding script for mint'
    parser = argparse.ArgumentParser(description=help)
    dr_help = "perform a Dry Run of the script, NOT WORKING YET"
    parser.add_argument('--dryrun', action="store_true", default=False,
                       help=dr_help)
    parser.add_argument('--gaming', action="store_true", default=False,
                       help='Install packages related to gaming')
    res = parser.parse_args()
    dry_run = res.dry_run

    # this is just for rc files and package managers
    if OS.contains('win'):
        print("Ooof, this isn't ready yet...")
    else:
        install_rc_files()
        run_brew_installs()
        configure_firefox()
        configure_freetube()
        configure_rss_reader()

    if OS.contains('linux'):
        run_apt_installs()
        run_snap_installs()
        run_flatpak_installs()


if __name__ == '__main__':
    main()
