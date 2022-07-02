#!/usr/bin/env python3
# Generic onboarding script for mac osx and debian
# jessebot@linux.com
import argparse
from configparser import ConfigParser
import getpass
import os
import shutil
import subprocess
import sys
import yaml
import wget
import zipfile

OS = sys.platform
USER_NAME = getpass.getuser()
HOME_DIR = os.getenv("HOME")
PWD = os.path.dirname(__file__)
PKG_MNGR_DIR = f"{PWD}/configs/installers"


def run_installer(installer="", extra_packages=[]):
    """
    Installs packages from one of the following installers: apt, snap, flatpak
    Takes an optional variable of extra_packages list to install optional
    packages for gaming or work tasks. Uses the yaml in configs/installers
    ---
    brew install from the brewfiles
    Takes opts, which is a string set to 'gaming', or 'work'
    Tested only on mac and linux, but maybe works for windows :shrug:
    """
    if installer == 'flatpak':
        subproc("sudo flatpak remote-add --if-not-exists flathub "
                "https://flathub.org/repo/flathub.flatpakrepo")

    if OS.__contains__('linux') and installer == 'brew':
        # on linux, just in case it's not in our path yet
        base_brew_cmd = ('/home/linuxbrew/.linuxbrew/bin/brew bundle '
                         f'--file={PKG_MNGR_DIR}/brew/Brewfile')

    with open(f'{PKG_MNGR_DIR}/packages.yml', 'r') as yaml_file:
        packages_dict = yaml.safe_load(yaml_file)[installer]

    emoji = packages_dict['emoji']
    status_msg = f" \033[94m {emoji} {installer} apps installing \033[00m"
    print(status_msg.center(70, '-'))

    installed_pkgs = subproc(packages_dict['list_cmd'], True, True)
    install_cmd = packages_dict['install_cmd']

    # Install default_packages always, but also install gaming or work
    pkg_types = ['default_packages']
    if extra_packages:
        pkg_types.extend(extra_packages)

    for pkg_list in pkg_types:
        for package in packages_dict[pkg_list]:
            if package in installed_pkgs:
                print(f'  {package} is already installed, continuing...')
            else:
                subproc(install_cmd + package)

    return None


def install_fonts():
    """
    This installs nerd fonts :)
    """
    if OS.__contains__('linux'):
        print("Installing fonts")
        url = ('https://github.com/source-foundry/Hack/releases/download/'
               'v3.003/Hack-v3.003-ttf.zip')
        downloaded_zip_file = wget.download(url)
        # unzip into our local font location
        with zipfile.ZipFile(downloaded_zip_file, 'r') as zip_ref:
            zip_ref.extractall(f'{HOME_DIR}/.local/share/fonts')


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
        # if overwrite set to True, delete the existing files first
        if overwrite:
            try:
                os.remove(hard_link)
            except Error as e:
                print('  ' + e)

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
    msg = "\033[94m Installing vim-plug, for vim plugins\033[00m "
    print(msg.center(70, '-'))
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
    repo_config_dir = f'{PWD}/configs/browser/firefox/extensions/'
    # different OS will have firefox profile info in different paths
    if OS.__contains__('linux'):
        ini_dir = f"{HOME_DIR}/.mozilla/Firefox/"
    elif OS == "darwin":
        ini_dir = f"{HOME_DIR}/Library/Application Support/Firefox/"

    msg = "\033[94m 🦊 Installing Firefox preferences and addons\033[00m "
    print(msg.center(70, '-'))

    print("  Checking Firefox profiles.ini for correct profile...")
    profile = ""
    configur = ConfigParser()
    configur.read(ini_dir + 'profiles.ini')
    sections = configur.sections()
    for section in sections:
        print('section: ' + section)
        if section.startswith('Install'):
            profile_dir = ini_dir + configur.get(section, 'Default')
            print("  Current firefox profile is in: " + profile)

    print("\n  Configuring Firefox user preferences...")
    usr_prefs = repo_config_dir.replace("extensions/", "user.js")
    shutil.copy(usr_prefs, profile_dir)
    print("\n  Finished copying over firefox settings :3")

    print("  Copying over firefox addons...")
    for addon_xpi in os.listdir(repo_config_dir):
        shutil.copy(repo_config_dir + addon_xpi,
                    f'{profile_dir}/extensions/')
    print("  Firefox extensions installed, but you still need to enable them.")

    return None


def subproc(cmd="", error_ok=False, suppress_output=False):
    """
    Takes a commmand to run in BASH, as well as optional error_ok bool to pass
    on errors in stderr/stdout
    """
    print(f'\n \033[92m Running cmd:\033[00m {cmd}')
    command = cmd.split()
    res_err = ''

    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    return_code = p.returncode
    res = p.communicate()
    res_stdout = '  ' + res[0].decode('UTF-8').replace('\n', '\n  ')
    res_stderr = '  ' + res[1].decode('UTF-8').replace('\n', '\n  ')

    # check return code, raise error if failure
    if not return_code or return_code != 0:
        # also scan both stdout and stdin for weird errors
        if "error" in res_stdout:
            res_err = f'stdout:\n{res_stdout}'
        elif "error" in res_stderr:
            res_err = res_err + f'stderr:\n{res_stderr}'

        if res_err and not error_ok:
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

    if not suppress_output:
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
    run_installer('brew', opts)
    hard_link_rc_files(overwrite_bool)
    install_fonts()
    configure_vim()

    if OS.__contains__('linux'):
        for installer in ['apt', 'snap', 'flatpak']:
            run_installer(installer, opts)

    # this can't be done until we have firefox, and who knows when that is
    configure_firefox()

    print("\033[92m SUCCESS \033[00m".center(70, '-'))
    print("\n Here's some stuff you gotta do manually:")
    print(" 🐋: Add your user to the docker group, and reboot")
    print(" 📰: Import rss feeds config into FluentReader or wherever")
    print(" 📺: Import subscriptions into FreeTube")
    print(" ⌨️ : Set capslock to control!")
    print(" ⏰: Install any cronjobs you need from the cron dir!")

    if OS == 'Darwin':
        print('Maybe also checkout: https://wangchujiang.com/awesome-mac/')


if __name__ == '__main__':
    main()
