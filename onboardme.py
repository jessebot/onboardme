#!/usr/bin/env python3
# Generic onboarding script for mac osx and debian
# jessebot@linux.com
import argparse
import getpass
import os
import shutil
import subprocess
import sys
import yaml
import wget

OS = sys.platform
USER_NAME = getpass.getuser()
HOME_DIR = os.getenv("HOME")
PWD = os.path.dirname(__file__)
PKG_DIR = f"{PWD}/packages"

with open(f'{PKG_DIR}/packages.yml', 'r') as yaml_file:
    PACKAGES = yaml.safe_load(yaml_file)


def run_apt_installs(opts=""):
    """
    install every apt package in packages/packages.yml
    """
    print(" 👻 \033[94m Apt packages installing \033[00m".center(70, '-'))
    for package in PACKAGES["apt"]:
        apt_install_cmd = f"apt install {package}"
        subproc(apt_install_cmd)

    # specific to gaming on linux
    if opts == "gaming":
        print("  - Installing gaming specific packaging...")
        for package in PACKAGES["apt_gaming"]:
            apt_install_cmd = f"apt install {package}"
            subproc(apt_install_cmd)

    return None


def run_flatpak_installs():
    """
    install every flatpak package in packages.yml
    """
    print(" 🫓 \033[94m Apt packages installing\033[00m".center(70, '-'))
    for package in PACKAGES["flatpak"]:
        flatpak_install_cmd = f"flatpak install {package}"
        subproc(flatpak_install_cmd)

    return None


def run_snap_installs():
    """
    install every snap package in packages.yml
    """
    print(" 🫰: \033[94m Snap apps installing...\033[00m ".center(70, '-'))
    for package in PACKAGES["snap"]:
        snap_install_cmd = f"snap install {package}"
        subproc(snap_install_cmd)

    return None


def run_brew_installs(opts=""):
    """
    brew install from the brewfiles
    Takes opts, which is a string set to 'gaming', or 'work'
    Tested only on mac and linux, but maybe works for windows :shrug:
    """
    print(" 🍺\033[94m Brew packages installing \033[00m".center(70, '-'))
    print("\n  You may be asked for your password for docker, and karabiner.")

    # this is the stuff that's installed on both mac and linux
    brew_cmd = f"brew bundle --file={PKG_DIR}/Brewfile_standard"
    subproc(brew_cmd)

    # install things for devops job
    if opts == "work":
        brew_cmd = f"brew bundle --file={PKG_DIR}/Brewfile_work"
        subproc(brew_cmd)

    # install linux specific apps
    if OS.__contains__('linux'):
        print(" - Installing 🐧 specific packaging...")
        brew_cmd = f"brew bundle --file={PKG_DIR}/Brewfile_linux"
        subproc(brew_cmd)
    # install mac specific apps
    elif OS == 'darwin':
        print(" 🍻 🍎\033[94m macOS specific brew packages installing \033[00m".center(70, '-'))
        brew_cmd = f"brew bundle --file={PKG_DIR}/Brewfile_mac"
        subproc(brew_cmd)

    return None


def run_upgrades():
    """
    run upgrade and update for every package manager
    """
    # apt
    apt_update_upgrade_cmd = f"apt upgrade && apt update"
    subproc(apt_update_upgrade_cmd)

    # brew
    brew_update_upgrade_cmd = f"brew upgrade && brew update"
    subproc(brew_update_upgrade_cmd)


def hard_link_rc_files():
    """
    Creates hardlinks to default rc files for vim, zsh, and bash in user's
    home directory. Uses hardlinks, so that if the link or onboardme repo files
    are removed, the data will remain.
    """
    print(" 🐚 \033[94m Shell and vim rc files installing..."
          "\033[00m".center(70, '-'))
    existing_files = []

    # loop through the rc_files and hard link them all to the user's home dir
    rc_dir = f'{PWD}/configs/rc_files'
    for rc_file in os.listdir(rc_dir):
        src_rc_file = f'{rc_dir}/{rc_file}'
        hard_link = f'{HOME_DIR}/{rc_file}'

        try:
            os.link(src_rc_file, hard_link)
            print(f'  Hard linked {hard_link}')

        except FileExistsError as error:
            # keep these for the end of the loop
            existing_files.append(hard_link)

        except PermissionError as error:
            # we keep going, because installing everything else is still useful
            print(f'  Permission error for: {src_rc_file} Error: {error}.')

    # create a bash_profile as well for macOS, and also just in case
    hard_link = f'{HOME_DIR}/.bash_profile'
    try:
        os.link(f'{rc_dir}/.bashrc', hard_link)
        print(f'  Hard linked {hard_link}')
    except FileExistsError as error:
        existing_files.append(hard_link)

    if existing_files:
        print(' 🤷 Looks like the following file(s) already exist:')
        for file in existing_files:
            print(f' - {file}')
        print('\nIf you want the links anyway, delete the files, and then '
              'rerun the script.')

    return None


def configure_vim():
    """
    Installs vim-plug, a plugin manager for vim, and then installs vim plugins,
    listed in ./config/rc_files/vim/.vimrc
    """
    print("\033[94m Installing vim-plug, for vim plugins\033[00m ".center(65,
                                                                          '-'))
    url = "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"
    plug_cmd = (f"curl -fLo {HOME_DIR}/.vim/autoload/plug.vim "
                f"--create-dirs {url}")
    subproc(plug_cmd)

    # this installs the vim plugins, can also use :PlugInstall in vim
    plugin_cmd = (f'vim -E -s -u "{HOME_DIR}/.vimrc" +PlugInstall +qall')
    subproc(plugin_cmd)

    return None


def configure_firefox():
    """
    Copies over default firefox settings and addons
    """
    # different os will have this in different places
    if platform == "linux" or platform == "linux2":
        # linux - untested
        PROFILE_PATH = (f"{HOME_DIR}/Firefox/Profiles/{FIREFOX_PROFILE}/")
    elif platform == "darwin":
        # OS X
        PROFILE_PATH = (f"{HOME_DIR}/Library/Application Support/Firefox/"
                        f"Profiles/{FIREFOX_PROFILE}/")
    elif platform == "win32" or platform == "windows":
        # Windows... - untested
        PROFILE_PATH = (f"{HOME_DIR}/Firefox/Profiles/{FIREFOX_PROFILE}/")

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
    print(f'\n \033[92m Running cmd:\033[00m {cmd}')
    command = cmd.split()
    res_err = ''

    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    return_code = p.returncode
    res = p.communicate()
    res_stdout = res[0].decode('UTF-8')
    res_stderr = res[1].decode('UTF-8')

    # check return code, raise error if failure
    if not return_code or return_code != 0:
        # also scan both stdout and stdin for weird errors
        if "error" in res_stdout:
            res_err = 'Output: {res_stdout}'
        elif "error" in res_stderr:
            res_err = res_err + 'Output: {res_stderr}'

        if res_err:
            err = (f'Return code was not zero! Error code: {return_code}')
            raise Exception(f'{err}\n{res_err}')

    if not res_stdout:
        return_str = '  ' + res_stderr.replace('\n','\n  ')
    else:
        return_str = '  ' + res_stdout.replace('\n','\n  ')

    print(return_str)
    return return_str


def main():
    """
    Core function
    """
    help = 'This is a generic onboarding script for mac and mint.'
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
    run_brew_installs(opts)
    hard_link_rc_files()
    configure_vim()
    # TODO: configure_firefox()

    if OS.__contains__('linux'):
        run_apt_installs(opts)
        run_snap_installs()
        run_flatpak_installs()

    print("\033[92m SUCCESS \033[00m".center(70,'-'))
    print("\n Here's some stuff you gotta do manually:")
    print(" 🐋: Add your user to the docker group, and reboot")
    print(" 📰: Import rss feeds config into FluentReader or wherever")
    print(" 📺: Import subscriptions into FreeTube")
    print(" 🦊: Install firefox config!")
    print(" ⌨️ : Set capslock to control!")
    print(" ⏰: Install any cronjobs you need from the cron dir!")


if __name__ == '__main__':
    main()
