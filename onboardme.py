#!/usr/bin/env python3.10
# Onboarding script for macOS and Debian by jessebot@Linux.com
from click import option, command, Choice
# from click import argument
from configparser import ConfigParser
import fileinput
from git import Repo
import os
from util.subproc_wrapper import subproc
from util.rich_click import RichCommand
from util.console_logging import print_panel, print_header, print_msg
from pathlib import Path
from random import randint
# rich helps pretty print everything
from rich import box, print
from rich.prompt import Confirm
from rich.table import Table
import shutil
import stat
import yaml
import wget


# run uname to get operating system and hardware info
SYSINFO = os.uname()
# this will be something like
OS = f"{SYSINFO.sysname}_{SYSINFO.machine}"
PWD = os.path.dirname(__file__)
HOME_DIR = os.getenv("HOME")
USER = os.getlogin()


def install_fonts():
    """
    This installs nerd fonts by wgetting the source archive and unextracting
    them into the user's local font directory. Runs fc-cache -fv to generate
    config, but you should still reboot when you're done :shrug:
    """
    if 'Linux' in OS:
        print_header('📝 [i]font[/i] installations')
        fonts_dir = f'{HOME_DIR}/repos/nerd-fonts'

        # do a shallow clone of the repo
        if not os.path.exists(fonts_dir):
            print_msg('[i]Downloading installer and font sets... ' +
                      '(can take a bit)')
            Path(fonts_dir).mkdir(parents=True, exist_ok=True)
            fonts_repo = 'https://github.com/ryanoasis/nerd-fonts.git'
            Repo.clone_from(fonts_repo, fonts_dir, depth=1)

        old_pwd = PWD
        os.chdir(fonts_dir)
        subproc('./install.sh Hack', False, True)
        subproc('./install.sh Mononoki', False, True)
        os.chdir(old_pwd)

        # debug: print(f'Going to remove {bitmap_conf} and link a yes map...')
        bitmap_conf = '/etc/fonts/conf.d/70-no-bitmaps.conf'

        # we do all of this with subprocess because I want the sudo prompt
        if os.path.exists(bitmap_conf):
            subproc(f'sudo rm {bitmap_conf}', False, True, False)

        subproc('sudo ln -s /etc/fonts/conf.avail/70-yes-bitmaps.conf '
                '/etc/fonts/conf.d/70-yes-bitmaps.conf', True, True, False)

        print_msg('[i][dim]The fonts should be installed, however, you have ' +
                  'to set your terminal font to the new font. I rebooted too.')


def link_dot_files(OS=OS, delete=False,
                   dot_files_dir=f'{PWD}/dot_files'):
    """
    Creates hard links to rc files for vim, zsh, bash, and hyper in user's
    home dir. Uses hard links, so that if the tt file is removed, the data
    will remain. If delete is True, we delete files before beginning.
    Takes optional dot_files_dir for special directory to grab files from
    """
    # table to print the results of all the files
    table = Table(expand=True,
                  box=box.MINIMAL_DOUBLE_HEAD,
                  row_styles=["", "dim"],
                  border_style="dim",
                  header_style="cornflower_blue",
                  title_style="light_steel_blue")
    table.add_column("File")
    table.add_column("Result", justify="center")

    # we only print this msg if we got the file exists error
    file_msg = False
    help_msg = ("If you want to [yellow]override[/yellow] the existing "
                "file, rerun script with the [b]--delete[/b] flag.")

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

            if os.path.exists(hard_link):
                # we check the inodes to see if the correct link has been made
                repo_stat = os.stat(src_dot_file)
                repo_inode = (repo_stat[stat.ST_INO], repo_stat[stat.ST_DEV])
                host_stat = os.stat(hard_link)
                host_inode = (host_stat[stat.ST_INO], host_stat[stat.ST_DEV])
                # we may have already created the link :)
                if repo_inode == host_inode or os.path.islink(src_dot_file):
                    table.add_row(f"[green]{hard_link}",
                                  "[green]Already linked ♥")
                else:
                    # if --delete was passed in to script
                    if delete:
                        os.remove(hard_link)
                        os.link(src_dot_file, hard_link)
            else:
                # try to hard link, but catch errors if delete set to False
                try:
                    os.link(src_dot_file, hard_link)
                except FileExistsError:
                    # keep till loop ends, to notify user no action was taken
                    table.add_row(f"[yellow]{hard_link}",
                                  "[yellow]File already exists 💔")
                    file_msg = True
                else:
                    table.add_row(f"[green]{hard_link}",
                                  "[green]Successfully linked ♥")

    print_panel(table, ":shell: Check if dot files are up to date", "left",
                "light_steel_blue")
    if file_msg:
        print('')
        print_msg(help_msg)


def configure_vim():
    """
    Installs vim-plug, vim plugin manager, and then installs vim plugins
    """
    print_header('[b]vim-plug[/b] and [green][i]Vim[/i][/green] plugins '
                 'installation [dim]and[/dim] upgrades')

    autoload_dir = f'{HOME_DIR}/.vim/autoload'
    url = 'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
    if not os.path.exists(autoload_dir):
        print_msg('[i]Creating directory structure and downloading [b]' +
                  'vim-plug[/b]...')
        Path(autoload_dir).mkdir(parents=True, exist_ok=True)
        wget.download(url, autoload_dir)

    # installs the vim plugins if not installed, updates vim-plug, and then
    # updates all currently installed plugins
    subproc('vim +PlugInstall +PlugUpgrade +PlugUpdate +qall!', False, True)
    print_msg('[i][dim]Plugins installed.')


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
        msg = f'{pkg_emoji} [green][b]{installer}[/b][/] app installations'
        print_header(msg)

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
            if f'{pkg_group}_packages' in installer_dict:

                if pkg_group != 'default':
                    msg = (f"Installing {pkg_group.replace('_', ' ')} "
                           f"{pkg_emoji} [b]{installer}[/b] packages")
                    print_header(msg, "cornflower_blue")

                for package in installer_dict[pkg_group + '_packages']:
                    if package not in installed_pkgs:
                        cmd = f'{install_cmd}{package}'
                        if installer == 'pip3.10':
                            cmd += ' --upgrade'
                        subproc(cmd, True, True)
                print_msg('[dim][i]Completed.')


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
        print_header("Installing default iTerm2 Dynamic Profile...")
        p = os.path.join(HOME_DIR,
                         'Library/Application Support/iTerm2/DynamicProfiles')
        shutil.copy(f'{PWD}/configs/iterm2/Profiles.json', p)
        print("")
        print_msg('[dim][i]Dynamic profile installed.')


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

    print_header('🦊 Installing Firefox preferences and addons')

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
    print_header("⌨️  Mapping capslock to control...")
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
    print_header('🛡️ Configuring Firewall...')
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
        print_header(f'[turquoise2]🐳 [dim]Adding[/dim] [b]{USER}[/b] '
                     '[dim]to[/dim] [b]docker[/b] [dim]group[/dim]')
        # default way for Linux systems
        cmd = f'sudo usermod -a -G docker {USER}'
        subproc(cmd, False, False, False)
        print("")
        print_msg(f'[dim][i][b]{USER}[/b] added to [b]docker[/b] group, but ' +
                  'you may still need to [b]reboot.')


def parse_local_configs():
    """
    parse the local config yaml file if it exists
    """
    local_config_dir = f'{HOME_DIR}/.config/onboardme/config.yaml'
    if os.path.exists(local_config_dir):
        with open(local_config_dir, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
    return config


def confirm_os_supported():
    """
    verify we're on a supported OS and ask to quit if not.
    """
    if SYSINFO.sysname != 'Linux' and SYSINFO.sysname != 'Darwin':
        print_panel(f"[magenta]{SYSINFO.sysname}[normal] isn't officially "
                    "supported. We haven't tested anything outside of Debian,"
                    "Ubuntu, and macOS.", "⚠️  [yellow]WARNING")

        quit_y = Confirm.ask("You're in uncharted waters. Do you wanna quit?")
        if quit_y:
            print_panel("That's probably safer. Have a safe day, friend.",
                        "Safety Award ☆")
            quit()
        else:
            print_panel("[red]Yeehaw, I guess.", "¯\\_(ツ)_/¯")
    else:
        print_panel("Operating System and Architechure [green]supported ♥",
                    "[cornflower_blue]Compatibility Check")


def setup_cronjobs():
    """
    setup any important cronjobs/alarms. Currently just adds nightly updates
    """
    print_header("⏰ Installing new cronjobs...")
    print("\n")


def print_manual_steps():
    """
    Just prints out the final steps to be done manually, til we automate them
    """
    end_msg = ("\n[i]Here's some stuff you gotta do manually (for now)[/]:\n\n"
               " 📰 - Import RSS feeds config into FluentReader\n"
               " 📺 [dim]- Import subscriptions into FreeTube \n[/]"
               " ⌨️  - Set CAPSLOCK to control!\n"
               " ⏰ [dim]- Install any cronjobs you need from the cron dir!\n"
               "   [/]- Source your bash config: [green]source .bashrc[/]\n"
               " 🐳 [dim]- Reboot, as [turquoise2]docker[/] demands it.\n\n[/]"
               "If there's anything else you need help with, check the docs:\n"
               "[dim]https://jessebot.github.io/onboardme")

    print_panel(end_msg, '[green]Success ♥')


def process_steps(only_steps=[], firewall=False, browser=False):
    """
    process which steps to run for which OS, which steps the user passed in,
    and then make sure dependent steps are always run.

    Returns a list of str type steps to run.
    """
    if only_steps:
        steps = list(only_steps)
        # setting up vim is useless if we don't have a .vimrc
        if 'vim_setup' in steps and 'dot_files' not in steps:
            steps.append('dot_files')
    else:
        steps = ['dot_files', 'install_upgrade_packages', 'vim_setup']

        # this is broken
        # if 'capslock_to_control' in steps:
        #     map_caps_to_control()

        # fonts are brew installed on macOS, docker group only applies to linux
        # currently don't have a great firewall on macOS outside of lulu
        if 'Linux' in OS:
            steps.extend(['font_installation', 'groups_setup'])
            if firewall:
                steps.append('firewall_setup')
            if browser:
                steps.append('browser_setup')
        # still use primarily iterm2 on macOS, and only macOS
        else:
            steps.append('iterm2_setup')

    return steps


# Click is so ugly, and I'm sorry we're using it for cli parameters here, but
# this allows us to use rich.click for pretty prettying the help interface
@command(cls=RichCommand)
@option('--delete', '-d',
        is_flag=True,
        help='Deletes existing rc files before creating hardlinks.')
@option('--extra_packages', '-e',
        type=Choice(['gaming', 'work']), multiple=True,
        help='Extra package groups to install. Accepts multiple groups.\n'
             'Ex: -e [cornflower_blue]work[/] -e [cornflower_blue]gaming')
@option('--browser', '-b',
        is_flag=True,
        help='Opt into [i]experimental[/i] Firefox configuruation.')
@option('--pkg_managers', '-p',
        default=None,
        multiple=True,
        metavar='PKG_MANAGER',
        type=Choice(['brew', 'pip3.10', 'apt', 'snap', 'flatpak']),
        help='Specific [light_steel_blue]PKG_MANAGER[/] to run. Defaults to '
             'only run brew, pip3, & ([i]if linux[/]) apt/snap/flatpak.\n'
             'Accepts multiple package managers. '
             'Ex: -p [cornflower_blue]brew[/] -p [cornflower_blue]apt')
@option('--only_steps', '-o',
        default=None,
        multiple=True,
        metavar='STEP',
        type=Choice(['dot_files', 'install_upgrade_packages', 'vim_setup']),
        help='[i]Beta[/i]. Only run [light_steel_blue]STEP[/] in the script. '
             'Accepts multiple steps.'
             '\nSteps include: dot_files, install_upgrade_packages, vim_setup.'
             '\nEx: -o [cornflower_blue]dot_files[/] -o '
             '[cornflower_blue]install_upgrade_packages')
@option('--firewall', '-f',
        is_flag=True,
        help='Setup SSH on a random port and add it to firewall.')
@option('--remote_host', '-H',
        multiple=True,
        metavar="IP_ADDRESS",
        default=None,
        help='Setup SSH on a random port and add [cornflower_blue]IP_ADDRESS'
             '[/] to firewall')
def main(delete: bool = False,
         extra_packages: str = "",
         browser: bool = False,
         pkg_managers: str = "",
         only_steps: str = "",
         firewall: bool = False,
         remote_host: str = ""):
    """
    Onboarding script for macOS and debian. Uses config in the script repo in
    package_managers/packages.yml. If run with no options on Linux it will
    install brew, apt, flatpak, and snap packages. On mac, only brew.
    coming soon: config via env variables and config files.
    """
    # before we do anything, we need to make sure this OS is supported
    confirm_os_supported()

    # figure out which steps to run:
    steps = process_steps(only_steps, firewall, browser)

    if 'dot_files' in steps:
        link_dot_files(delete)

    if 'font_installation' in steps:
        install_fonts()

    # if user specifies, only do packages passed into --package_managers
    if 'install_upgrade_packages' in steps:
        if pkg_managers:
            default_installers = pkg_managers
        else:
            default_installers = ['brew', 'pip3.10']
            if 'Linux' in OS:
                default_installers.extend(['apt', 'snap', 'flatpak'])

        # process additional package lists, if any
        package_groups = ['default']
        if extra_packages:
            package_groups.extend(extra_packages)

        run_installers(default_installers, package_groups)

    if 'firewall_setup' in steps:
        if remote_host:
            # will also configure ssh if you specify --remote
            # configure_ssh()
            configure_firewall(remote_host)

    if 'iterm2' in steps:
        # configure the iterm2 if we're on macOS
        configure_terminal(OS)

    if 'vim_setup' in steps:
        # this installs the vim plugins
        configure_vim()

    if 'groups_setup' in steps:
        # will add your user to docker group
        setup_nix_groups()

    print_manual_steps()


if __name__ == '__main__':
    main()
