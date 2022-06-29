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


def run_apt_installs(opts=""):
    """
    install every apt package in packages.yaml
    """
    for package in CONFIG_FILE["apt"]:
        apt_install_cmd = f"apt install {package}"
        result = subproc(apt_install_cmd)

    # specific to gaming on linux
    if opts == "gaming":
        for package in CONFIG_FILE["apt_gaming"]:
            apt_install_cmd = f"apt install {package}"
            result = subproc(apt_install_cmd)

    return None


def run_flatpak_installs():
    """
    install every flatpak package in packages.yaml
    """
    for package in CONFIG_FILE["flatpak"]:
        flatpak_install_cmd = f"flatpak install {package}"
        result = subproc(flatpak_install_cmd)

    return None


def run_snap_installs():
    """
    install every snap package in packages.yaml
    """
    for package in CONFIG_FILE["snap"]:
        snap_install_cmd = f"snap install {package}"
        result = subproc(snap_install_cmd)

    return None


def run_brew_installs(opts=""):
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

    # install things for devops job
    if opts == "work":
        brew_cmd = "brew bundle --file=./packages/Brewfile_work"
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
    # apt
    apt_update_upgrade_cmd = f"apt upgrade && apt update"
    result = subproc(apt_update_upgrade_cmd)

    # brew
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
    parser.add_argument('--work', action="store_true", default=False,
                       help='Install packages related to devops stuff')
    res = parser.parse_args()
    dry_run = res.dry_run
    gaming = res.gaming
    work = res.work
    if work:
        opts = "work"
    elif gaming:
        opts = "gaming"
    else:
        opts = ""

    if OS.contains('win'):
        print("Ooof, this isn't ready yet...")
        print("But you can check out the docs/windows directory for "
              "help getting set up!")
        return

    # installs bashrc and the like
    install_rc_files()
    run_brew_installs(opts)
    configure_firefox()

    if OS.contains('linux'):
        run_apt_installs(opts)
        run_snap_installs()
        run_flatpak_installs()

    print("All done! here's some stuff you gotta do manually:")
    print("🐋: Add your user to the docker group, and reboot")
    print("📰: Import rss feeds config into FluentReader or wherever")
    print("📺: Import subscriptions into FreeTube")
    print("Install any cronjobs you need from the cron dir!")


if __name__ == '__main__':
    main()
