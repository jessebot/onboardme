#!/usr/bin/env python3
# Generic onboarding script for macOS and Debian by jessebot@linux.com
from argparse import ArgumentParser
from configparser import ConfigParser
import fileinput
from git import Repo
import os
from pathlib import Path
from random import randint
import shutil
import subprocess
import sys
import yaml
import wget
OS = sys.platform
HOME_DIR = os.getenv("HOME")
PWD = os.path.dirname(__file__)


def run_installers(installers=['brew'], pkg_groups=['default']):
    """
    Installs packages with apt, brew, snap, flatpak. If no installers list
    passed in, only use brew for mac. Takes optional variable, pkg_group_lists
    to install optional packages.
    """
    pkg_manager_dir = f'{PWD}/configs/installers/'
    with open(pkg_manager_dir + 'packages.yml', 'r') as yaml_file:
        installers_list = yaml.safe_load(yaml_file)

    # just in case we got any duplicates, we iterate through this as a set
    for installer in set(installers):
        installer_dict = installers_list[installer]
        emoji = installer_dict['emoji']
        print_head(f'{emoji} {installer} apps installing')

        install_cmd = installer_dict['install_cmd']
        installed_pkgs = subproc(installer_dict['list_cmd'], True, True)

        # Brew: still using bundle files, so this is a little weird
        if installer == 'brew':
            install_cmd += pkg_manager_dir + 'brew/'
            if OS == 'darwin':
                pkg_groups.append('mac')

        # Flatpak: requires us add flathub remote repo manually
        if installer == 'flatpak':
            subproc('sudo flatpak remote-add --if-not-exists flathub '
                    'https://flathub.org/repo/flathub.flatpakrepo')

        for pkg_group in pkg_groups:
            if pkg_group + '_packages' in installer_dict:
                if pkg_group != 'default':
                    print_head(f'Installing {pkg_group} {installer} packages')
                for package in installer_dict[pkg_group + '_packages']:
                    if package in installed_pkgs:
                        print(f'  {package} is already installed, continuing.')
                    else:
                        subproc(f'{install_cmd}' + package, True)


def install_fonts():
    """
    This installs nerd fonts by wgetting the source archive and unextracting
    them into the user's local font directory. Runs fc-cache -fv to generate
    config, but you should still reboot when you're done :shrug:
    """
    if 'linux' in OS:
        print_head('✍️  Installing fonts...')
        fonts_dir = f'{HOME_DIR}/repos/nerd-fonts'

        # do a shallow clone of the repo
        if not os.path.exists(fonts_dir):
            print('  Downloading installer and font sets...  (can take a bit)')
            Path(fonts_dir).mkdir(parents=True, exist_ok=True)
            fonts_repo = 'https://github.com/ryanoasis/nerd-fonts.git'
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


def hard_link_rc_files(delete=False):
    """
    Creates hardlinks to rc files for vim, zsh, bash, and hyper in user's
    home dir. Uses hardlinks, so that if the target file is removed, the data
    will remain. If delete is True, we delete files before beginning.
    """
    print_head(' 🐚 Shell and vim rc files installing...')
    existing_files = []

    # loop through the rc_files and hard link them all to the user's home dir
    rc_dir = f'{PWD}/configs/rc_files'
    for rc_file in os.listdir(rc_dir):
        src_rc_file = f'{rc_dir}/{rc_file}'
        hard_link = f'{HOME_DIR}/{rc_file}'

        try:
            if delete and os.path.exists(hard_link):
                os.remove(hard_link)

            os.link(src_rc_file, hard_link)
            print(f'  Hard linked {hard_link}')
        except FileExistsError:
            # keep till loop ends, to notify user that no action was taken
            existing_files.append(hard_link)
        except PermissionError as error:
            print(f'  Permission error for: {src_rc_file} Error: {error}.')

    if existing_files:
        print('  Looks like the following file(s) already exist:')
        for file in existing_files:
            print(f' - {file}')
        print('\n If you want the links anyway, rerun script with --delete')


def configure_vim():
    """
    Installs vim-plug, vim plugin manager, and then installs vim plugins
    """
    print_head('Installing vim-plug, for vim plugins')

    autoload_dir = f'{HOME_DIR}/.vim/autoload'
    url = 'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
    if not os.path.exists(autoload_dir):
        print('  Creating directory structure and downloading vim-plug...')
        Path(autoload_dir).mkdir(parents=True, exist_ok=True)
        wget.download(url, autoload_dir)

    # this installs the vim plugins, can also use :PlugInstall in vim
    plugin_cmd = (f'vim -E -s -u "{HOME_DIR}/.vimrc" +PlugInstall +qall')
    subproc(plugin_cmd)


def configure_firefox():
    """
    Copies over default firefox settings and addons
    """
    # different OS will have firefox profile info in different paths
    if 'linux' in OS:
        ini_dir = f'{HOME_DIR}/.mozilla/firefox/'
    elif OS == 'darwin':
        # hate apple for their capitalized directories
        ini_dir = f'{HOME_DIR}/Library/Application Support/Firefox/'

    print_head('🦊 Installing Firefox preferences and addons')

    print('  Checking Firefox profiles.ini for correct profile...')
    profile_dir = ''
    prof_config = ConfigParser()
    prof_config.read(ini_dir + 'profiles.ini')

    sections = prof_config.sections()
    for section in sections:
        if section.startswith('Install'):
            profile_dir = ini_dir + prof_config.get(section, 'Default')
            print('  Current firefox profile is in: ' + profile_dir)

    repo_config_dir = f'{PWD}/configs/browser/firefox/extensions/'

    print('\n  Configuring Firefox user preferences...')
    usr_prefs = repo_config_dir.replace('extensions/', 'user.js')
    shutil.copy(usr_prefs, profile_dir)
    print('  Finished copying over firefox settings :3')

    print('\n  Copying over firefox addons...')
    for addon_xpi in os.listdir(repo_config_dir):
        shutil.copy(repo_config_dir + addon_xpi,
                    f'{profile_dir}/extensions/')
    print('  Firefox extensions installed, but they need to be enabled\n')


def map_caps_to_control():
    """
    Maps capslock to control. This is ugly and awful
    """
    cmd = ("sudo gsettings set org.gnome.desktop.input-sources "
           """xkb-options '["caps:ctrl_modifier"]'""")
    subproc(cmd)


def configure_ssh():
    """
    This will setup SSH for you on a semi-random port that probably isn't taken
    """
    random_port = randint(2224, 2260)
    print(f'  Setting SSHD port to {random_port}')
    sshd_config = fileinput.input('/etc/ssh/sshd_config', inplace=True)

    for line in sshd_config:
        if '#Port ' in line:
            print(f'Port {random_port}', end='')
        elif '#PasswordAuthentication ' in line:
            print('PasswordAuthentication no')
        elif '#PubkeyAuthentication' in line:
            print('PubkeyAuthentication no')
        else:
            print(line)

    sshd_config.append('Match Group ssh')
    sshd_config.append('  PubkeyAuthentication yes')


def configure_firewall(remote_hosts=[]):
    """
    configure iptables
    """
    print_head('🛡️ Configuring Firewall...')
    if remote_hosts:
        remote_ips = ' '.join(remote_hosts)
        subproc(f'{PWD}/configs/firewall/iptables.sh {remote_ips}')
    else:
        subproc(f'{PWD}/configs/firewall/no_ssh_iptables.sh')


def subproc(command="", error_ok=False, suppress_output=False):
    """
    Takes a str commmand to run in BASH, as well as optionals bools to pass on
    errors in stderr/stdout and suppress_output
    """
    print(f'\n \033[92m Running cmd:\033[00m {command}')
    cmd = command.split()
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return_code = p.returncode
    res = p.communicate()
    res_stdout = '  ' + res[0].decode('UTF-8').replace('\n', '\n  ')
    res_stderr = '  ' + res[1].decode('UTF-8').replace('\n', '\n  ')

    if not error_ok:
        # check return code, raise error if failure
        if not return_code or return_code != 0:
            # also scan both stdout and stdin for weird errors
            for output in [res_stdout.lower(), res_stderr.lower()]:
                if 'error' in output:
                    err = f'Return code not zero! Return code: {return_code}'
                    raise Exception(f'\033[0;33m {err} \n {output} \033[00m')

    for output in [res_stdout, res_stderr]:
        if output:
            if not suppress_output:
                print(output)
            return output


def print_head(status=""):
    """
    takes a string and prints it pretty
    """
    print(f'\033[92m {status} \033[00m'.center(80, '-'))


def parse_args():
    """
    Parse arguments and return dict
    """
    d_help = 'Deletes existing rc files before creating hardlinks. BE CAREFUL!'
    e_help = ('Extra package groups to install. Accepts multiple args, e.g. '
              '--extra gaming')
    i_help = ('Installers to run. Accepts multiple args, e.g. only run brew '
              'and apt: --installers brew apt')
    h_help = 'Add IP to firewall for remote access'
    p = ArgumentParser(description=main.__doc__)

    p.add_argument('--delete', action='store_true', default=False, help=d_help)
    p.add_argument('-e', '--extra', default=None, nargs='+', help=e_help)
    p.add_argument('-f', '--firefox', action='store_true', default=False,
                   help='Opt into experimental firefox configuring')
    p.add_argument('-i', '--installers', default=None, nargs='+', help=i_help)
    p.add_argument('-r', '--remote', action='store_true', default=False,
                   help='Setup SSH on a random port and add it to firewall.')
    p.add_argument('-H', '--host', nargs='+', default=None, help=h_help)
    return p.parse_args()


def main():
    """
    Onboarding script for macOS and debian. Uses config in the script repo in
    configs/installers/packages.yml. If run with no options on Linux it will
    install brew, apt, flatpak, and snap packages. On mac, only brew.
    """
    opt = parse_args()

    print('\n 🥱 This could take a while on a fresh install, so settle in and '
          'get comfy 🛋️ \n')
    hard_link_rc_files(opt.delete)
    install_fonts()

    # process additional package lists, if any
    package_groups = ['default']
    if opt.extra:
        package_groups.extend(opt.extra)

    default_installers = ['brew']
    if 'linux' in OS:
        default_installers.extend(['apt', 'snap', 'flatpak'])
        map_caps_to_control()
        if opt.firefox:
            configure_firefox()

    # if user specifies, only do packages passed into --installers
    if opt.installers:
        default_installers = opt.installers

    run_installers(default_installers, package_groups)

    # this will also configure ssh if you specify --remote
    if opt.remote and 'linux' in OS:
        # configure_ssh()
        configure_firewall(opt.host)

    # this is SUPPOSED to install the vim plugins, but sometimes does not
    configure_vim()

    print_head('❇️  SUCCESS ❇️ ')
    print("\n Here's some stuff you gotta do manually:")
    print(' 📰: Import RSS feeds config into FluentReader or wherever')
    print(' 📺: Import subscriptions into FreeTube')
    print(' ⌨️ : Set capslock to control!')
    print(' ⏰: Install any cronjobs you need from the cron dir!')
    print(' 💲: Source your .bashrc')
    print(' 🐋: Add your user to the docker group, and reboot')


if __name__ == '__main__':
    main()
