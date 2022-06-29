#!/usr/bin/env python3
# Generic onboarding script for mac osx and debian
# jessebot@linux.com
import argparse
import getpass
import os
import shutil
import subprocess
import sys
from sys import platform
import yaml

USER_NAME = getpass.getuser()
HOME_DIR = os.getenv("HOME")
OS = platform
CONFIG_FILE = "packages/packages.yml"

with open(CONFIG_FILE, 'r') as yaml_file:
    PACKAGES = yaml.safe_load(yaml_file)


def run_apt_installs(opts=""):
    """
    install every apt package in packages.yaml
    """
    print(" 👻 Apt packages installing 👻 ".center(70,'-'))
    for package in PACKAGES["apt"]:
        apt_install_cmd = f"apt install {package}"
        result = subproc(apt_install_cmd)
        print(result)

    # specific to gaming on linux
    if opts == "gaming":
        print("  Installing gaming specific packaging...")
        for package in PACKAGES["apt_gaming"]:
            apt_install_cmd = f"apt install {package}"
            result = subproc(apt_install_cmd)
            print(result)

    print(" 👻 Apt packages INSTALLED 👻 ".center(70,'-'))
    print("")
    return None


def run_flatpak_installs():
    """
    install every flatpak package in packages.yaml
    """
    print(" 🫓 Apt packages installing 🫓 ".center(70,'-'))
    for package in PACKAGES["flatpak"]:
        flatpak_install_cmd = f"flatpak install {package}"
        result = subproc(flatpak_install_cmd)

    print(" 🫓 Apt packages INSTALLED 🫓 ".center(70,'-'))
    print("")
    return None


def run_snap_installs():
    """
    install every snap package in packages.yaml
    """
    print(" 🫰: Snap apps installing... 🫰: ".center(70,'-'))
    for package in PACKAGES["snap"]:
        snap_install_cmd = f"snap install {package}"
        result = subproc(snap_install_cmd)
    print(" 🫰: Snap apps INSTALLED 🫰: ".center(70,'-'))
    print("")

    return None


def run_brew_installs(opts=""):
    """
    brew install from the brewfiles
    """
    print(" 🍻 Brew packages installing... 🍻 ".center(70, '-'))
    # make sure brew is installed
    url = "https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh"
    install_cmd = f'/bin/bash -c "$(curl -fsSL {url})"'
    result = subproc(install_cmd)
    print(result)

    # this is the stuff that's installed on both mac and linux
    brew_cmd = "brew bundle --file=./packages/Brewfile_standard"
    result = subproc(brew_cmd)
    print(result)

    # install things for devops job
    if opts == "work":
        brew_cmd = "brew bundle --file=./packages/Brewfile_work"
        result = subproc(brew_cmd)
        print(result)

    # install linux specific apps
    if OS.__contains__('linux'):
        print("  Installing 🐧 specific packaging...")
        brew_cmd = "brew bundle --file=./packages/Brewfile_linux"
        result = subproc(brew_cmd)
        print(result)
    # install mac specific apps
    elif OS == 'darwin':
        print("  Installing 🍎 specific packaging...")
        brew_cmd = "brew bundle --file=./packages/Brewfile_mac"
        result = subproc(brew_cmd)
        print(result)
    
    print(" 🍻 Brew packages INSTALLED 🍻 ".center(70, '-'))
    print("")

    return None


def run_upgrades():
    """
    run upgrade and update for every package manager
    """
    # apt
    apt_update_upgrade_cmd = f"apt upgrade && apt update"
    result = subproc(apt_update_upgrade_cmd)
    print(result)

    # brew
    brew_update_upgrade_cmd = f"brew upgrade && brew update"
    result = subproc(brew_update_upgrade_cmd)
    print(result)


def install_rc_files():
    """
    Copies over default rc files for vim, zsh, and bash
    """
    print(" 🐚 Shell and vim rc files installing... 🐚 ".center(70,'-'))
    rc_dirs = ['zsh','bash','vim']
    for rc_dir in rc_dirs:
        for rc_file in os.listdir(f'./configs/rc_files/{rc_dir}'):
            try:
                os.link(f'./configs/rc_files/{rc_dir}/{rc_file}',
                        f'{HOME_DIR}/{rc_file}')
                print(f'Linked {HOME_DIR}/{rc_file}')
            except FileExistsError as error:
                print(f'  {HOME_DIR}/{rc_file} already exists, continuing...')

    # Install the vim plugin manager
    print("  Installing a vim plugin manager")
    vim_plug_cmd = ("curl -fLo ~/.vim/autoload/plug.vim --create-dirs "
        "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim")
    res =  subproc(vim_plug_cmd)
    print(res)

    print(" 🐚 Shell and vim rc files INSTALLED 🐚 ".center(70,'-'))
    print("")
    return None


def configure_firefox():
    """
    Copies over default firefox settings and addons 
    """
    # different os will have this in different places
    if platform == "linux" or platform == "linux2":
        # linux - untested
        PROFILE_PATH=(f"/home/{USER_NAME}/Firefox/Profiles/{FIREFOX_PROFILE}/")
    elif platform == "darwin":
        # OS X
        PROFILE_PATH=(f"/Users/{USER_NAME}/Library/Application Support/Firefox/"
                      f"Profiles/{FIREFOX_PROFILE}/")
    elif platform == "win32" or platform == "windows":
        # Windows... - untested
        PROFILE_PATH=(f"/Users/{USER_NAME}/Library/Application Support/Firefox/"
                      f"Profiles/{FIREFOX_PROFILE}/")

    shutil.copy('configs/browser/firefox/user.js', PROFILE_PATH)

    shutil.copytree('configs/browser/firefox/distribution/extensions/',
                    PROFILE_PATH + 'extensions/')

    print("Copied over firefox settings")
    return None


def subproc(cmd, help="Something went wrong!"):
    """
    Takes a commmand to run in BASH, as well as optional
    help text, both str
    """
    print(f'  Running cmd: {cmd}')
    command = cmd.split()
    res_err = ''
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
    help = 'This is a generic onboarding script for mint and mac.'
    parser = argparse.ArgumentParser(description=help)
    dr_help = "perform a Dry Run of the script, NOT WORKING YET"
    parser.add_argument('--dry', action="store_true", default=False,
                       help=dr_help)
    parser.add_argument('--gaming', action="store_true", default=False,
                       help='Install packages related to gaming')
    parser.add_argument('--work', action="store_true", default=False,
                       help='Install packages related to devops stuff')
    res = parser.parse_args()
    dry_run = res.dry
    gaming = res.gaming
    work = res.work
    if work:
        opts = "work"
    elif gaming:
        opts = "gaming"
    else:
        opts = ""

    if OS == 'win32' or OS == 'windows':
        print("Ooof, this isn't ready yet...")
        print("But you can check out the docs/windows directory for "
              "help getting set up!")
        return

    # installs bashrc and the like
    install_rc_files()
    run_brew_installs(opts)
    # TODO: configure_firefox()

    if OS.__contains__('linux'):
        run_apt_installs(opts)
        run_snap_installs()
        run_flatpak_installs()

    print("All done! here's some stuff you gotta do manually:")
    print(" 📝: run :plugInstall in vim to install vim plugins")
    print(" 🐋: Add your user to the docker group, and reboot")
    print(" 📰: Import rss feeds config into FluentReader or wherever")
    print(" 📺: Import subscriptions into FreeTube")
    print(" 🦊: Install firefox config!")
    print(" ⌨️ : Set capslock to control!")
    print(" ⏰: Install any cronjobs you need from the cron dir!")


if __name__ == '__main__':
    main()
