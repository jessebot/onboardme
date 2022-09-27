#!/usr/bin/env python3.10
# Onboarding script for macOS and Debian by jessebot@linux.com
from argparse import ArgumentParser
from configparser import ConfigParser
import fileinput
from git import Repo
import os
from pathlib import Path
from random import randint
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table
import shutil
import subprocess
import yaml
import wget


# run uname to get operating system and hardware info
SYSINFO = os.uname()
# this will be something like
OS = f"{SYSINFO.sysname}_{SYSINFO.machine}"
PWD = os.path.dirname(__file__)
HOME_DIR = os.getenv("HOME")
USER = os.getlogin()
# this is for rich text, to pretty print things
CONSOLE = Console()


def install_fonts():
    """
    This installs nerd fonts by wgetting the source archive and unextracting
    them into the user's local font directory. Runs fc-cache -fv to generate
    config, but you should still reboot when you're done :shrug:
    """
    if 'linux' in OS:
        CONSOLE.rule('✍️  Installing fonts...')
        fonts_dir = f'{HOME_DIR}/repos/nerd-fonts'

        # do a shallow clone of the repo
        if not os.path.exists(fonts_dir):
            print('  Downloading installer and font sets...  (can take a bit)')
            Path(fonts_dir).mkdir(parents=True, exist_ok=True)
            fonts_repo = 'https://github.com/ryanoasis/nerd-fonts.git'
            Repo.clone_from(fonts_repo, fonts_dir, depth=1)

        old_pwd = PWD
        os.chdir(fonts_dir)
        subproc('./install.sh Hack')
        subproc('./install.sh mononoki')
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


def hard_link_dot_files(OS="", delete=False,
                        dot_files_dir=f'{PWD}/configs/dot_files'):
    """
    Creates hard links to rc files for vim, zsh, bash, and hyper in user's
    home dir. Uses hard links, so that if the target file is removed, the data
    will remain. If delete is True, we delete files before beginning.
    Takes optional dot_files_dir for special directory to grab files from
    """
    # table to print the results of all the files
    table = Table(title=":shell: Linking dot files...", expand=True)
    table.add_column("File", style="cyan")
    table.add_column("Result", justify="center")

    # we only print this msg if we got the file exists error
    print_msg = False
    help_msg = ("[i][yellow]Failures are likely due to the files already ."
                "If you want to override the existing files, rerun script "
                "with the --delete flag")

    # loop through the dot_files and hard link them all to the user's home dir
    for root, dirs, files in os.walk(dot_files_dir):

        # make sure the directory structure matches in ~/.config
        for config_dir in dirs:
            full_path = os.path.join(root, config_dir)
            full_home_path = full_path.replace(dot_files_dir, HOME_DIR)
            Path(full_home_path).mkdir(parents=True, exist_ok=True)

        # then add each file to the list of files to hardlink
        for config_file in files:
            src_dot_file = os.path.join(root, config_file)
            hard_link = src_dot_file.replace(dot_files_dir, HOME_DIR)

            # try to hard link here, but catch errors if delete set to False
            try:
                # if delete has been passed in, delete the existing file first
                if delete and os.path.exists(hard_link):
                    if not os.path.islink(hard_link):
                        os.remove(hard_link)

                os.link(src_dot_file, hard_link)
                table.add_row(f"[green]{hard_link}",
                              "[green]Success :green_heart:")

            except FileExistsError:
                # keep till loop ends, to notify user that no action was taken
                table.add_row(f"[magenta]{hard_link}",
                              "[magenta]File already exists")
                print_msg = True

    print(table)
    if print_msg:
        print(help_msg)


def configure_vim():
    """
    Installs vim-plug, vim plugin manager, and then installs vim plugins
    """
    print("\n")
    CONSOLE.rule('Installing vim-plug, for vim plugins')

    autoload_dir = f'{HOME_DIR}/.vim/autoload'
    url = 'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
    if not os.path.exists(autoload_dir):
        print('  Creating directory structure and downloading vim-plug...')
        Path(autoload_dir).mkdir(parents=True, exist_ok=True)
        wget.download(url, autoload_dir)

    # this installs the vim plugins, can also use :PlugInstall in vim
    plugin_cmd = ('vim +PlugInstall +qall')
    subproc(plugin_cmd)


def run_installers(installers=['brew'], pkg_groups=['default']):
    """
    Installs packages with apt, brew, snap, flatpak. If no installers list
    passed in, only use brew for mac. Takes optional variable, pkg_group_lists
    to install optional packages.
    """
    pkg_manager_dir = f'{PWD}/package_managers/'
    with open(pkg_manager_dir + 'packages.yml', 'r') as yaml_file:
        installers_list = yaml.safe_load(yaml_file)

    # just in case we got any duplicates, we iterate through this as a set
    for installer in set(installers):
        installer_dict = installers_list[installer]
        pkg_emoji = installer_dict['emoji']
        print("\n")
        CONSOLE.rule(f'{pkg_emoji} {installer} apps installing')

        install_cmd = installer_dict['install_cmd']
        installed_pkgs = subproc(installer_dict['list_cmd'], True, True)

        # Brew and python: still using bundle files, and requirements.txt
        for special_pkg in ['brew', 'pip3.10']:
            if installer == special_pkg:
                file_path = os.path.join(PWD, pkg_manager_dir, special_pkg)
                install_cmd += file_path + '/'
                if 'Darwin' in OS and special_pkg == 'brew':
                    pkg_groups.append('🍎_macOS')

        # Flatpak: requires us add flathub remote repo manually
        if installer == 'flatpak':
            subproc('sudo flatpak remote-add --if-not-exists flathub '
                    'https://flathub.org/repo/flathub.flatpakrepo')

        for pkg_group in pkg_groups:
            if pkg_group + '_packages' in installer_dict:
                if pkg_group != 'default':
                    print("\n")
                    CONSOLE.rule(f"Installing {pkg_group.replace('_', ' ')} "
                                 f"{pkg_emoji} {installer} packages")
                for package in installer_dict[pkg_group + '_packages']:
                    if package in installed_pkgs:
                        print(f'  {package} is already installed, continuing.')
                    else:
                        cmd = f'{install_cmd}{package}'
                        if installer == 'pip3.10':
                            cmd += ' --upgrade'
                        subproc(cmd, True)


def configure_feeds():
    """
    configures feeds like freetube and RSS readers
    """
    # freeTube is weird, requires this name and directory to work smoothly
    subs_db = '{PWD}/configs/feeds/freetube/subscriptions.db'
    shutil.copy(subs_db, f'{HOME_DIR}/Downloads/subscriptions.db')


def configure_terminal(OS='Darwin'):
    """
    configure colorschemes and dynamic profiles for iterm2 if we're on macOS
    """
    if "Darwin" in OS:
        print("\n")
        print(Panel("Installing default Dynamic Profile...",
                    title="[green]iTerm2"))
        p = os.path.join(HOME_DIR,
                         'Library/Application Support/iTerm2/DynamicProfiles')
        shutil.copy(f'{PWD}/configs/iterm2/Profiles.json', p)


def configure_firefox():
    """
    Copies over default firefox settings and addons
    """
    # different OS will have firefox profile info in different paths
    if 'Linux' in OS:
        ini_dir = f'{HOME_DIR}/.mozilla/firefox/'
    elif OS == 'darwin':
        # hate apple for their capitalized directories
        ini_dir = f'{HOME_DIR}/Library/Application Support/Firefox/'

    CONSOLE.rule('🦊 Installing Firefox preferences and addons')

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
    print('  Firefox extensions installed, but they need to be enabled.')


def map_caps_to_control():
    """
    Maps capslock to control. This is ugly and awful
    """
    CONSOLE.rule("⌨️  Mapping capslock to control...")
    cmd = "setxkbmap -layout us -option ctrl:nocaps"
    subproc(cmd, True, True)


def configure_ssh():
    """
    This will setup SSH for you on a semi-random port that probably isn't taken
    """
    # it's not a huge list right now, but it's better than just 22 or 2222
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
    TODO: Add Lulu configuration
    """
    CONSOLE.rule('🛡️ Configuring Firewall...')
    if remote_hosts:
        remote_ips = ' '.join(remote_hosts)
        subproc(f'{PWD}/configs/firewall/iptables.sh {remote_ips}')
    else:
        subproc(f'{PWD}/configs/firewall/no_ssh_iptables.sh')


def setup_nix_groups():
    """
    Set up any groups, at this time just docker, and add current user to them
    """
    # mac is weird...
    # cmd = f"sudo dseditgroup -o edit -a {USER} -t user docker"

    if "Linux" in OS:
        print("\n")
        CONSOLE.rule(f'[bright_cyan]🐳 Adding {USER} to docker group')
        # default way for linux systems
        cmd = f'sudo usermod -a -G docker {USER}'
        subproc(cmd)
        print('[i]User added to docker group, but you still need to reboot.')


def subproc(command="", error_ok=False, suppress_output=False):
    """
    Takes a str commmand to run in BASH, as well as optionals bools to pass on
    errors in stderr/stdout and suppress_output
    """
    cmd = command.split()
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return_code = p.returncode
    res = p.communicate()
    res_stdout = res[0].decode('UTF-8')
    res_stderr = res[1].decode('UTF-8')

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
                print(Panel(output, title='[green]Run cmd:[normal] ' +
                            command))
            return output


def parse_local_configs():
    """
    parse the local config yaml file if it exists
    """
    local_config_dir = f'{HOME_DIR}/.config/onboardme/config.yaml'
    if os.path.exists(local_config_dir):
        with open(local_config_dir, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
    return config


def parse_args():
    """
    Parse arguments and return dict
    """
    d_help = 'Deletes existing rc files before creating hardlinks. BE CAREFUL!'
    df_help = ('COMING SOON. Git url to clone for dot files, assumes dot files'
               'are in root directory for now')
    e_help = ('Extra package groups to install. Accepts multiple args, e.g. '
              '--extra gaming')
    i_help = ('Installers to run. Accepts multiple args. Defaults to only run '
              'brew, pip3, and apt(if linux). example: --installers brew apt')
    o_help = ('Experimental. Only run these steps in the script, e.g. --only '
              'dot_files. Steps include dot_files, and package_managers.')
    h_help = 'Add IP to firewall for remote access'
    p = ArgumentParser(description=main.__doc__)

    p.add_argument('--dot_files', default=None, nargs='+', help=df_help)
    p.add_argument('-d', '--delete', action='store_true', default=False,
                   help=d_help)
    p.add_argument('-e', '--extra', default=None, nargs='+', help=e_help)
    p.add_argument('-f', '--firefox', action='store_true', default=False,
                   help='Opt into experimental firefox configuring')
    p.add_argument('-i', '--installers', default=None, nargs='+', help=i_help)
    p.add_argument('-o', '--only', default=None, nargs='+', help=o_help)
    p.add_argument('-r', '--remote', action='store_true', default=False,
                   help='Setup SSH on a random port and add it to firewall.')
    p.add_argument('-H', '--host', nargs='+', default=None, help=h_help)

    return p.parse_args()


def confirm_os_supported():
    """
    verify we're on a supported OS and ask to quit if not.
    """
    if SYSINFO.sysname != 'Linux' and SYSINFO.sysname != 'Darwin':
        print(Panel(f"[magenta]{SYSINFO.sysname}[normal] isn't officially "
                    "supported. We haven't tested anything outside of Debian,"
                    "Ubuntu, and macOS.", title="⚠️  [yellow]WARNING"))

        quit_y = Confirm.ask("You're in uncharted waters. Do you wanna quit?")
        if quit_y:
            print(Panel("That's probably safer. Have a safe day, friend."))
            quit()
        else:
            print(Panel("[red]Yeehaw, I guess.", title="¯\\_(ツ)_/¯"))
    else:
        print("\n")
        print(Panel("Operating System and Architechure [green]supported ♥",
                    title="[purple]Compatibility Check"))
        print("\n")


def setup_cronjobs():
    """
    setup any important cronjobs/alarms. Currently just adds nightly updates
    """
    print("\n")
    CONSOLE.rule("⏰ Installing new cronjobs...")
    print("\n")


def main():
    """
    Onboarding script for macOS and debian. Uses config in the script repo in
    package_managers/packages.yml. If run with no options on Linux it will
    install brew, apt, flatpak, and snap packages. On mac, only brew.
    coming soon: config via env variables and config files.
    """
    # before we do anything, we need to make sure this OS is supported
    confirm_os_supported()

    # then procress all the options passed in
    opt = parse_args()

    hard_link_dot_files(OS, opt.delete)
    if opt.only and 'dot_files' in opt.only:
        if len(opt.only) == 1:
            exit()

    # fonts are brew installed unless we're on linux
    if 'linux' in OS:
        install_fonts()

    # process additional package lists, if any
    package_groups = ['default']
    if opt.extra:
        package_groups.extend(opt.extra)

    # Pip currently just gets you powerline :)
    default_installers = ['brew', 'pip3.10']
    if 'linux' in OS:
        default_installers.extend(['apt', 'snap', 'flatpak'])
        # this is broken
        # map_caps_to_control()
        if opt.firefox:
            configure_firefox()

    # if user specifies, only do packages passed into --installers
    if opt.installers:
        default_installers = opt.installers

    print("\n")
    msg = ":yawning_face: This could take a while on a fresh install."
    print(Panel(msg, title="[purple]Beginning Package Installations",
                subtitle="[purple][bold]Settle In & Get Comfy"))

    run_installers(default_installers, package_groups)

    # will also configure ssh if you specify --remote
    if opt.remote and 'linux' in OS:
        # not sure what's up with this...
        # configure_ssh()
        configure_firewall(opt.host)

    # configure the iterm2 if we're on macOS
    configure_terminal(OS)

    # this is SUPPOSED to install the vim plugins, but sometimes does not
    configure_vim()

    # will add your user to linux groups such as docker
    setup_nix_groups()

    print("\n")
    CONSOLE.rule('❇️  SUCCESS ❇️ ')
    print("Here's some stuff you gotta do manually:")
    print(' 📰: Import RSS feeds config into FluentReader or wherever')
    print(' 📺: Import subscriptions into FreeTube')
    print(' ⌨️ : Set capslock to control!')
    print(' ⏰: Install any cronjobs you need from the cron dir!')
    print(' 💲: Source your bash config: source .bashrc')
    print(' 🐋: Reboot, as the whale demands it \n')

    print("If there's anything else you need help with, check the docs here:")
    print("https://jessebot.github.io/onboardme/")


if __name__ == '__main__':
    main()
