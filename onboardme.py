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


def run_linux_installer(installer="", extra_packages=[]):
    """
    Installs packages from one of the following installers: apt, snap, flatpak
    Takes an optional variable of extra_packages list to install optional
    packages for gaming or work tasks. Uses the yaml in packages/packages.yml
    """
    with open(f'{PKG_DIR}/packages.yml', 'r') as yaml_file:
        packages_dict = yaml.safe_load(yaml_file)

    # -y is assume yes for "are you sure you want to install"
    if installer == 'apt':
        emoji = "🫠"
        ls_installed = 'apt list --installed | cut -d '/' -f 1 | grep -v error'
        installed = subproc(ls_installed)
        installer_cmd = f"sudo apt-get install -y "
    elif installer == 'flatpak':
        emoji = "🫓"
        currently_installed = subproc('flatpak list --columns=application')
        installer_cmd = f"flatpak install -y flathub "
        subproc("sudo flatpak remote-add --if-not-exists flathub "
                "https://flathub.org/repo/flathub.flatpakrepo")
    elif installer == 'snap':
        emoji = "🫰 "
        currently_installed = subproc('snap list')
        installer_cmd = f"sudo snap install "
    else:
        print(f'INVALID INSTALLER: {installer}')
        return None

    # Install default_packages always, but also install gaming or work
    pkg_lists = ['default_packages']
    if extra_packages:
        pkg_lists.extend(extra_packages)

    for pkg_list in pkg_lists:
        for package in packages_dict[installer][pkg_list]:
            print(f" {emoji} \033[94m {installer} apps "
                   "installing...\033[00m ".center(70, '-'))
            if package not in currently_installed:
                subproc(installer_cmd + package)
            else:
                print(f'  {package} is already installed, continuing...')

    return None


def run_brew_installs(opts=""):
    """
    brew install from the brewfiles
    Takes opts, which is a string set to 'gaming', or 'work'
    Tested only on mac and linux, but maybe works for windows :shrug:
    """
    print(" 🍺\033[94m Brew packages installing \033[00m".center(70, '-'))
    if OS.__contains__('linux'):
        # on linux, just in case it's not in our path, but it's in our .bashrc
        base_brew_cmd = ('/home/linuxbrew/.linuxbrew/bin/brew bundle '
                         f'--file={PKG_DIR}')
    else:
        base_brew_cmd = f'brew bundle --file={PKG_DIR}'

    # this is the stuff that's installed on both mac and linux
    brew_cmd = f"{base_brew_cmd}/Brewfile_standard"
    subproc(brew_cmd)

    # install things for devops job
    if opts == "work":
        brew_cmd = f"{base_brew_cmd}/Brewfile_work"
        subproc(brew_cmd)

    # install linux specific apps
    if OS.__contains__('linux'):
        print(" - Installing 🐧 specific packaging...")
        brew_cmd = f"{base_brew_cmd}/Brewfile_linux"
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


def hard_link_rc_files(overwrite=False):
    """
    Creates hardlinks to default rc files for vim, zsh, and bash in user's
    home directory. Uses hardlinks, so that if the link or onboardme repo files
    are removed, the data will remain. If overwrite is set to True, we delete
    files before beginning.
    """
    print(" 🐚 \033[94m Shell and vim rc files installing..."
          "\033[00m".center(70, '-'))
    existing_files = []

    # loop through the rc_files and hard link them all to the user's home dir
    rc_dir = f'{PWD}/configs/rc_files'
    for rc_file in os.listdir(rc_dir):
        src_rc_file = f'{rc_dir}/{rc_file}'
        hard_link = f'{HOME_DIR}/{rc_file}'
        if overwrite:
            try:
                os.remove(hard_link)
            except:
                pass

        try:
            os.link(src_rc_file, hard_link)
            print(f'  Hard linked {hard_link}')

        except FileExistsError as error:
            # keep till loop ends, to notify user to clean up if they want
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
    if OS.__contains__('linux'):
        plugin_cmd = ('/home/linuxbrew/.linuxbrew/bin/vim -E -s -u '
                      f'"{HOME_DIR}/.vimrc" +PlugInstall +qall')

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


def subproc(cmd=""):
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
    res_stdout = '  ' + res[0].decode('UTF-8').replace('\n','\n  ')
    res_stderr = '  ' + res[1].decode('UTF-8').replace('\n','\n  ')

    # check return code, raise error if failure
    if not return_code or return_code != 0:
        # also scan both stdout and stdin for weird errors
        if "error" in res_stdout:
            res_err = f'stdout:\n{res_stdout}'
        elif "error" in res_stderr:
            res_err = res_err + f'stderr:\n{res_stderr}'

        if res_err:
            err = (f'Return code was not zero! Error code: {return_code}')
            # hacky, but whatevs
            if 'flathub' in res_err:
                print(f' {err} \n {res_err} \nIf this is flatpak related, try'
                       ' a reboot, or verify package name on flathub.org/apps')

            else:
                raise Exception(f' {err} \n {res_err}')

    if not res_stdout:
        return_str = res_stder
    else:
        return_str = res_stdout

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
    parser.add_argument('--overwrite', action="store_true", default=False,
                        help='Deletes existing rc files, such as .bashrc, '
                             'before creating hardlinks. Be careful!')
    res = parser.parse_args()
    dry_run = res.dry
    gaming = res.gaming
    work = res.work
    overwrite_bool = res.overwrite
    opts = []
    if work:
        opts.append("work")
    elif gaming:
        opts.append("gaming")

    if OS == 'win32' or OS == 'windows':
        print("Ooof, this isn't ready yet...")
        print("But you can check out the docs/windows directory for "
              "help getting set up!")
        return

    # installs bashrc and the like
    run_brew_installs(opts)
    hard_link_rc_files(overwrite_bool)
    configure_vim()
    # TODO: configure_firefox()

    if OS.__contains__('linux'):
        run_linux_installer('apt', opts)
        run_linux_installer('snap', opts)
        run_linux_installer('flatpak', opts)

    print("\033[92m SUCCESS \033[00m".center(70,'-'))
    print("\n Here's some stuff you gotta do manually:")
    print(" 🐋: Add your user to the docker group, and reboot")
    print(" 📰: Import rss feeds config into FluentReader or wherever")
    print(" 📺: Import subscriptions into FreeTube")
    print(" 🦊: Install firefox config!")
    print(" ⌨️ : Set capslock to control!")
    print(" ⏰: Install any cronjobs you need from the cron dir!")

    if OS == 'Darwin':
        print('Maybe also checkout: https://wangchujiang.com/awesome-mac/')


if __name__ == '__main__':
    main()
