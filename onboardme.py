#!/usr/bin/env python3
# Generic onboarding script for macOS and Debian
# jessebot@linux.com
import argparse
from configparser import ConfigParser
from git import Repo
import os
from pathlib import Path
import shutil
import subprocess
import sys
import yaml
import wget
OS = sys.platform
if OS.__contains__('linux'):
    OS = 'linux'
HOME_DIR = os.getenv("HOME")
PWD = os.path.dirname(__file__)


def run_installers(installers=['brew'], pkg_lists=['default']):
    """
    Installs packages with apt, appimage, brew, snap, flatpak. If no installers
    list passed in, will do only brew for mac, but all for linux. Takes an
    optional variable of pkg_lists to install optional packages for work/gaming
    """
    print("\n 🥱 ⚠️  If this is a fresh install of your OS, this could take a"
          "while. Settle in and get comfy 🛋️ \n")

    # just in case we got any duplicates, we iterate through this as a set
    for installer in set(installers):
        pkgs = pkg_lists
        if installer == 'flatpak':
            subproc("sudo flatpak remote-add --if-not-exists flathub "
                    "https://flathub.org/repo/flathub.flatpakrepo")

        pkg_manager_dir = f"{PWD}/configs/installers/"
        with open(pkg_manager_dir + 'packages.yml', 'r') as yaml_file:
            packages_dict = yaml.safe_load(yaml_file)[installer]

        emoji = packages_dict['emoji']
        status_msg = f" \033[94m {emoji} {installer} apps installing \033[00m"
        print(status_msg.center(80, '-'))

        installed_pkgs = subproc(packages_dict['list_cmd'], True, True)
        install_cmd = packages_dict['install_cmd']

        # For brew, we're still using bundle files, so this is a little weird
        if installer == 'brew':
            install_cmd += pkg_manager_dir + 'brew/'
            if OS == 'linux':
                pkgs.append('linux')
            elif OS == 'darwin':
                pkgs.append('mac')

        for pkg_list in pkgs:
            if pkg_list != 'default':
                msg = f"Installing {pkg_list} specific {installer} packages..."
                print(f" {msg} ".center(80, '-'))
            for package in packages_dict[pkg_list + '_packages']:
                if package in installed_pkgs:
                    print(f'  {package} is already installed, continuing...')
                else:
                    subproc(f'{install_cmd}' + package)
    return None


def install_fonts():
    """
    This installs nerd fonts by wgetting the source archive and unextracting
    them into the user's local font directory. Runs fc-cache -fv to generate
    config, but you should still reboot when you're done :shrug:
    """
    if OS == 'linux':
        status_msg = "\033[94m ✍️  Installing fonts... \033[00m"
        print(status_msg.center(80, '-'))
        fonts_dir = f'{HOME_DIR}/repos/nerd-fonts'

        # do a shallow clone of the repo
        if not os.path.exists(fonts_dir):
            print("  Downloading installer and font sets...  (can take a bit)")
            Path(fonts_dir).mkdir(parents=True, exist_ok=True)
            fonts_repo = "https://github.com/ryanoasis/nerd-fonts.git"
            Repo.clone_from(fonts_repo, fonts_dir, depth=1)

        print('  Running the font installer...')
        old_pwd = PWD
        os.chdir(fonts_dir)
        subproc('./install.sh Hack')
        os.chdir(old_pwd)

        bitmap_conf = '/etc/fonts/conf.d/70-no-bitmaps.conf'
        print(f'  Going to remove {bitmap_conf} and link a yes map...')

        # we do all of this with subprocess because I want the sudo prompt
        if os.path.exists(bitmap_conf):
            subproc(f'sudo rm {bitmap_conf}')

        subproc('sudo ln -s /etc/fonts/conf.avail/70-yes-bitmaps.conf '
                '/etc/fonts/conf.d/70-yes-bitmaps.conf', True, False)

        print('\n  The fonts should be installed, however, you have to set '
              'your terminal font to the new font. I rebooted too.')
    return None


def hard_link_rc_files(overwrite=False):
    """
    Creates hardlinks to default rc files for vim, zsh, and bash in user's
    home directory. Uses hardlinks, so that if the link or onboardme repo files
    are removed, the data will remain. If overwrite is set to True, we delete
    files before beginning.
    """
    print(" 🐚 \033[94m Shell and vim rc files installing..."
          "\033[00m".center(80, '-'))
    existing_files = []

    # loop through the rc_files and hard link them all to the user's home dir
    rc_dir = f'{PWD}/configs/rc_files'
    for rc_file in os.listdir(rc_dir):
        src_rc_file = f'{rc_dir}/{rc_file}'
        hard_link = f'{HOME_DIR}/{rc_file}'

        # if overwrite set to True, delete the existing files first
        if overwrite:
            if os.path.exists(hard_link):
                os.remove(hard_link)

        try:
            os.link(src_rc_file, hard_link)
            print(f'  Hard linked {hard_link}')

        except FileExistsError:
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
    except FileExistsError:
        existing_files.append(hard_link)

    if existing_files:
        print("  Looks like the following file(s) already exist:")
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
    print(msg.center(80, '-'))

    autoload_dir = f'{HOME_DIR}/.vim/autoload'
    url = "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"
    if not os.path.exists(autoload_dir):
        print("  Creating directory structure and downloading vim-plug...")
        Path(autoload_dir).mkdir(parents=True, exist_ok=True)
        wget.download(url, autoload_dir)

    # this installs the vim plugins, can also use :PlugInstall in vim
    plugin_cmd = (f'vim -E -s -u "{HOME_DIR}/.vimrc" +PlugInstall +qall')
    subproc(plugin_cmd)

    return None


def configure_firefox():
    """
    Copies over default firefox settings and addons
    """
    # different OS will have firefox profile info in different paths
    if OS == 'linux':
        ini_dir = f"{HOME_DIR}/.mozilla/firefox/"
    elif OS == 'darwin':
        # hate apple for their capitalized directories
        ini_dir = f"{HOME_DIR}/Library/Application Support/Firefox/"

    msg = "\033[94m 🦊 Installing Firefox preferences and addons\033[00m "
    print(msg.center(80, '-'))

    print("  Checking Firefox profiles.ini for correct profile...")
    profile_dir = ""
    prof_config = ConfigParser()
    prof_config.read(ini_dir + 'profiles.ini')

    sections = prof_config.sections()
    for section in sections:
        if section.startswith('Install'):
            profile_dir = ini_dir + prof_config.get(section, 'Default')
            print("  Current firefox profile is in: " + profile_dir)

    repo_config_dir = f'{PWD}/configs/browser/firefox/extensions/'

    print("\n  Configuring Firefox user preferences...")
    usr_prefs = repo_config_dir.replace("extensions/", "user.js")
    shutil.copy(usr_prefs, profile_dir)
    print("  Finished copying over firefox settings :3")

    print("\n  Copying over firefox addons...")
    for addon_xpi in os.listdir(repo_config_dir):
        shutil.copy(repo_config_dir + addon_xpi,
                    f'{profile_dir}/extensions/')
    print("  Firefox extensions installed, but they need to be enabled\n")

    return None


def map_caps_to_control():
    """
    maps capslock to control
    """
    if OS == 'linux':
        # god this is ugly and awful
        cmd = ("sudo gsettings set org.gnome.desktop.input-sources "
               """xkb-options '["caps:ctrl_modifier"]'""")
        subproc(cmd)


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
        return_str = res_stderr
    else:
        return_str = res_stdout

    if not suppress_output:
        print(return_str)
    return return_str


def main():
    """
    This calls the arg parser and all the core functions above
    """
    help = ('This is a generic onboarding script for macOS and debian. It uses'
            'a config in the script repo directory under configs/installers'
            'If you run this with no options on macOS, it will install all '
            'default brew packages, and updated you rc_files. On Linux it will'
            ' do the same, but it will also install apt, flatpak, snap '
            ' packages, plus it will configure firefox. For optional'
            "packages, example for gaming and work -e/--extras gaming work")
    parser = argparse.ArgumentParser(description=help)

    dr_help = "perform a Dry Run of the script, NOT WORKING YET"
    parser.add_argument('--dry', action="store_true", default=False,
                        help=dr_help)

    e_msg = ("Takes optional package lists to install, accepts multiple, "
             "example: --extra gaming")

    parser.add_argument('-e', '--extra', type=str, default=None, nargs="+",
                        help=e_msg)

    i_msg = ('ONLY install packages from these installers. experimental, '
             'accepts multiple args  example: --installers brew apt')
    parser.add_argument('--installers', type=str, default=None, nargs="+",
                        help=i_msg)

    parser.add_argument('--firefox', action="store_true", default=False,
                        help='Opt into experimental firefox configuring')

    parser.add_argument('--overwrite', action="store_true", default=False,
                        help='Deletes existing rc files, such as .bashrc, '
                             'before creating hardlinks. Be careful!')
    res = parser.parse_args()
    overwrite_bool = res.overwrite

    # process additional package lists, if any
    packages = ['default']
    if res.extra:
        packages.extend(res.extra)

    default_installers = ['brew']
    if OS == 'linux':
        default_installers.extend(['apt', 'snap', 'flatpak'])

    # if user specifies, only do packages passed into --installers
    if res.installers:
        default_installers = res.installers

    # runs installers for brew, apt, etc...
    run_installers(default_installers, packages)

    # installs bashrc and the like
    hard_link_rc_files(overwrite_bool)

    # fun icons related to vim and lsd
    install_fonts()

    # this is SUPPOSED to install the vim plugins, but sometimes does not
    configure_vim()

    # currently broken
    map_caps_to_control()

    # this can't be done until we have firefox, and who knows when that is
    if res.firefox:
        configure_firefox()

    print("\033[92m SUCCESS \033[00m".center(80, '-'))
    print("\n Here's some stuff you gotta do manually:")
    print(" 🐋: Add your user to the docker group, and reboot")
    print(" 📰: Import rss feeds config into FluentReader or wherever")
    print(" 📺: Import subscriptions into FreeTube")
    print(" ⌨️ : Set capslock to control!")
    print(" ⏰: Install any cronjobs you need from the cron dir!")

    if OS == 'darwin':
        print('\nMaybe also checkout: https://wangchujiang.com/awesome-mac/')


if __name__ == '__main__':
    main()
