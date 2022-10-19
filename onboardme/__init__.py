#!/usr/bin/env python3.10
# Onboarding script for macOS and Debian by jessebot@Linux.com
from click import option, command, Choice
from configparser import ConfigParser
import fileinput
from git import Repo
from git import RemoteProgress
import logging
import os
from pathlib import Path
from random import randint
# rich helps pretty print everything
from rich import box, print
from rich.prompt import Confirm
from rich.table import Table
from rich.logging import RichHandler
import shutil
from .util.subproc import subproc
from .util.rich_click import RichCommand
from .util.console_logging import print_panel, print_header, print_msg
import yaml
import wget

# logging
FORMAT = "%(message)s"
# run uname to get operating system and hardware info
SYSINFO = os.uname()
# this will be something like Darwin_x86_64
OS = f"{SYSINFO.sysname}_{SYSINFO.machine}"
PWD = os.path.dirname(__file__)
HOME_DIR = os.getenv("HOME")
USER = os.getlogin()


def setup_dot_files(OS='Linux', delete=False, dot_files_git_url=""):
    """
    note on how we're doing things, seperate dot files repo:
    https://probablerobot.net/2021/05/keeping-'live'-dotfiles-in-a-git-repo/
    """
    if not dot_files_git_url:
        dot_files_git_url = "https://github.com/jessebot/dot_files"

    git_dir = os.path.join(HOME_DIR, '.git_dot_files')
    cmds = [f'git --git-dir="{git_dir}" --work-tree="{HOME_DIR}" init',
            f'git --git-dir="{git_dir}" config status.showUntrackedFiles no',
            f'git --git-dir="{git_dir}" remote add origin {dot_files_git_url}',
            f'git --git-dir="{git_dir}" fetch']

    if delete:
        # WARN: The next command will overwrite local files with remote files
        cmds.append(f'git --git-dir="{git_dir}" reset --hard origin/main')
        file_msg = False
    else:
        file_msg = True
        # we only print this msg if we got the file exists error
        help_msg = ("If you want to [yellow]override[/yellow] the existing "
                    "file(s), rerun script with the [b]--delete[/b] flag.")

    subproc(cmds, False, False, True, HOME_DIR)

    # table to print the results of all the files
    table = Table(expand=True,
                  box=box.MINIMAL_DOUBLE_HEAD,
                  row_styles=["", "dim"],
                  border_style="dim",
                  header_style="cornflower_blue",
                  title_style="light_steel_blue")

    table.add_column("Remote Dot Files")

    table.add_row("[green]", "[green]Already linked ♥")
    # keep till loop ends, to notify user no action was taken
    table.add_row("[yellow]", "[yellow]File already exists 💔")

    print_panel(table, ":shell: Check if dot files are up to date", "left",
                "light_steel_blue")
    if file_msg:
        print('')
        print_msg(help_msg)
    return


def brew_install_upgrade(OS="Darwin", pkg_groups=['default']):
    """
    Run the install/upgrade of packages managed by brew, also updates brew
    Always installs the .Brewfile (which has libs that work on both mac/linux)
    Accepts args:
        * OS     - string arg of either Darwin or Linux
        * devops - bool, installs devops brewfile, defaults to false
    """
    brew_msg = '🍺 [green][b]brew[/b][/] app Installs/Upgrades'
    print_header(brew_msg)

    install_cmd = "brew bundle --quiet"

    subproc(['brew update --quiet', 'brew upgrade --quiet',
             f'{install_cmd} --global'])

    # the above is basically our default
    pkg_groups.remove('default')

    # install os specific or package group specific brew stuff
    brewfile = os.path.join(PWD, 'config/brew/Brewfile_')
    # sometimes there isn't an OS specific brewfile, but there always is 4 mac
    os_brewfile = os.path.exists(brewfile + OS)
    if os_brewfile or pkg_groups:
        install_cmd += f" --file={brewfile}"

        if os_brewfile:
            os_msg = f'[i][dim][b]{OS}[/b] specific ' + brew_msg
            print_msg(os_msg)
            subproc([f'{install_cmd}{OS}'], True)

        if pkg_groups:
            for group in pkg_groups:
                msg = group.title + ' specific ' + brew_msg
                print_header(msg)
                subproc([f'{install_cmd}{group}'], True)

    # cleanup operation doesn't seem to happen automagically :shrug:
    cleanup_msg = '[i][dim]🍺 [green][b]brew[/b][/] final upgrade/cleanup'
    print_msg(cleanup_msg)
    subproc(['brew cleanup'])

    print_msg('[dim][i]Completed.')
    return


def run_pkg_mngrs(pkg_mngrs=['brew', 'pip3.10', 'apt', 'snap', 'flatpak'],
                  pkg_groups=['default']):
    """
    Installs packages with apt, brew, snap, flatpak. If no pkg_mngrs list
    passed in, only use brew for mac. Takes optional variable, pkg_group_lists
    to install optional packages.
    """
    # brew has a special flow with brew files
    if 'brew' in pkg_mngrs:
        brew_install_upgrade(SYSINFO.sysname, pkg_groups)
        pkg_mngrs.remove('brew')

    if 'Darwin' in OS:
        if 'pip3.10' not in pkg_mngrs:
            return
        else:
            pkg_mngrs = ['pip3.10']

    with open(f'{PWD}/config/packages.yml', 'r') as yaml_file:
        pkg_mngrs_list = yaml.safe_load(yaml_file)

    # just in case we got any duplicates, we iterate through pkg_mngrs as a set
    for pkg_mngr in set(pkg_mngrs):
        pkg_mngr_dict = pkg_mngrs_list[pkg_mngr]
        pkg_emoji = pkg_mngr_dict['emoji']
        msg = f'{pkg_emoji} [green][b]{pkg_mngr}[/b][/] app Installs'
        print_header(msg)

        # run package manager specific setup if needed, and updates/upgrades
        pkg_cmds = pkg_mngr_dict['commands']
        for pre_cmd in ['setup', 'update', 'upgrade']:
            if pre_cmd in pkg_cmds:
                subproc([pkg_cmds[pre_cmd]], False, True)

        # This is the list of currently installed packages
        installed_pkgs = subproc([pkg_cmds['list']], True, True)
        # this is the list of should be installed packages
        required_pkgs = pkg_mngr_dict['packages']

        # iterate through package groups, such as: default, gaming, devops...
        for pkg_group in pkg_groups:
            if required_pkgs[pkg_group]:
                if pkg_group != 'default':
                    msg = (f"Installing {pkg_group.replace('_', ' ')} "
                           f"{pkg_emoji} [b]{pkg_mngr}[/b] packages")
                    print_header(msg, "cornflower_blue")

                for package in required_pkgs[pkg_group]:
                    if package not in installed_pkgs:
                        cmd = pkg_cmds['install'] + package
                        subproc([cmd], True, True)
                print_msg('[dim][i]Completed.')
    return


def install_fonts():
    """
    Clones nerd-fonts repo and does a sparse checkout on only mononoki and
    hack fonts. Also removes 70-no-bitmaps.conf and links 70-yes-bitmaps.conf
    Then runs install.sh from nerd-fonts repo
    """
    if 'Linux' in OS:
        print_header('📝 [i]font[/i] installations')
        fonts_dir = f'{HOME_DIR}/repos/nerd-fonts'

        # do a shallow clone of the repo
        if not os.path.exists(fonts_dir):
            # log.debug('Nerdfonts require some setup on Linux...')
            bitmap_conf = '/etc/fonts/conf.d/70-no-bitmaps.conf'
            # log.debug(f'Going to remove {bitmap_conf} and link a yes map...')
            # we do all of this with subprocess because I want the sudo prompt
            if os.path.exists(bitmap_conf):
                subproc([f'sudo rm {bitmap_conf}'], False, True, False)

            subproc(['sudo ln -s /etc/fonts/conf.avail/70-yes-bitmaps.conf ' +
                    '/etc/fonts/conf.d/70-yes-bitmaps.conf'],
                    True, True, False)

            print_msg('[i]Downloading installer and font sets... ')

            Path(fonts_dir).mkdir(parents=True, exist_ok=True)
            fonts_repo = 'https://github.com/ryanoasis/nerd-fonts.git'

            class CloneProgress(RemoteProgress):
                def update(self, op_code, cur_count, max_count=None,
                           message=''):
                    if message:
                        log.info(message)

            Repo.clone_from(fonts_repo, fonts_dir, progress=CloneProgress(),
                            multi_options=['--sparse', '--filter=blob:none'])
            subproc(["git sparse-checkout add patched-fonts/Mononoki",
                     "git sparse-checkout add patched-fonts/Hack"], False,
                    False, True, fonts_dir)
        else:
            subproc(["git pull"], False, False, True, fonts_dir)

        subproc(['./install.sh Hack', './install.sh Mononoki'], False, True,
                True, fonts_dir)

        print_msg('[i][dim]The fonts should be installed, however, you have ' +
                  'to set your terminal font to the new font. I rebooted too.')
        return


def vim_setup():
    """
    Installs vim-plug, vim plugin manager, and then installs vim plugins
    """
    print_header('[b]vim-plug[/b] and [green][i]Vim[/i][/green] plugins '
                 'installation [dim]and[/dim] upgrades')

    # trick to not run youcompleteme init every single time
    init_ycm = False
    if not os.path.exists(f'{HOME_DIR}/.vim/plugged/YouCompleteMe/install.py'):
        init_ycm = True

    # this is for installing vim-plug
    autoload_dir = f'{HOME_DIR}/.vim/autoload'
    url = 'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
    if not os.path.exists(autoload_dir):
        print_msg('[i]Creating directory structure and downloading [b]' +
                  'vim-plug[/b]...')
        Path(autoload_dir).mkdir(parents=True, exist_ok=True)
        wget.download(url, autoload_dir)

    # installs the vim plugins if not installed, updates vim-plug, and then
    # updates all currently installed plugins
    subproc(['vim +PlugInstall +PlugUpgrade +PlugUpdate +qall!'], False, True)
    print_msg('[i][dim]Plugins installed.')

    if init_ycm:
        # This is for you complete me, which is a python completion module
        subproc(f'{HOME_DIR}/.vim/plugged/YouCompleteMe/install.py')

    return


def configure_feeds():
    """
    configures feeds like freetube and RSS readers
    """
    # freeTube is weird, requires this name and directory to work smoothly
    subs_db = '{PWD}/configs/feeds/freetube/subscriptions.db'
    shutil.copy(subs_db, f'{HOME_DIR}/Downloads/subscriptions.db')


def configure_firefox():
    """
    Copies over default firefox settings and addons
    """
    # different OS will have firefox profile info in different paths
    if 'Linux' in OS:
        ini_dir = f'{HOME_DIR}/.mozilla/firefox/'
    elif 'Darwin' in OS:
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
    subproc(["setxkbmap -layout us -option ctrl:nocaps"])


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
    TODO: Add Lulu configuration!
    """
    print_header('🛡️ Configuring Firewall...')
    if remote_hosts:
        remote_ips = ' '.join(remote_hosts)
        cmd = f'{PWD}/configs/firewall/iptables.sh {remote_ips}'
        configure_ssh()
    else:
        cmd = f'{PWD}/configs/firewall/no_ssh_iptables.sh'
    subproc([cmd])


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
        subproc([cmd], False, False, False)
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
               "[cyan][link=https://jessebot.github.io/onboardme]"
               "jessebot.github.io/onboardme[/link]")

    print_panel(end_msg, '[green]♥ ˖⁺‧Success‧⁺˖ ♥')


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

    return steps


def process_user_config(delete_existing, git_clone_url, log_level,
                        pkg_managers, pkg_groups, silent, remote_host):
    """
    process the config in ~/.config/onboardme/config.yml if it exists
    and return variables as a dict for use in script, else return default opts
    """
    cli_dict = {'dot_files': {'delete_existing': delete_existing,
                              'git_clone_url': git_clone_url},
                'pkg_managers': {'enabled': pkg_managers,
                                 'pkg_groups': pkg_groups},
                'log_level': log_level,
                'silent': silent,
                'remote_host': remote_host}

    # cli options are more important, but if none passed in, we check .config
    usr_cfg_file = os.path.join(HOME_DIR, '.config/onboardme/config.yml')

    if not os.path.exists(usr_cfg_file):
        return cli_dict
    else:
        with open(usr_cfg_file, 'r') as yaml_file:
            user_prefs = yaml.safe_load(yaml_file)

        for key in cli_dict.keys():
            if key not in user_prefs.keys():
                user_prefs[key] = cli_dict[key]
            elif cli_dict[key]:
                user_prefs[key] = cli_dict[key]

            # make sure the dict is not nested...
            if type(user_prefs[key]) == dict:
                for nested_key in user_prefs[key].keys():
                    if nested_key not in user_prefs[key].keys():
                        user_prefs[key][nested_key] = cli_dict[key][nested_key]
                    elif cli_dict[key][nested_key]:
                        user_prefs[key][nested_key] = cli_dict[key][nested_key]

        return user_prefs


# Click is so ugly, and I'm sorry we're using it for cli parameters here, but
# this allows us to use rich.click for pretty prettying the help interface
@command(cls=RichCommand)
# each of these is an option in the cli and variable we use later on
@option('--browser', '-b',
        is_flag=True,
        help='Opt into [i]experimental[/i] Firefox configuruation.')
@option('--delete_existing', '-d',
        is_flag=True,
        help='Deletes existing rc files before creating hardlinks.')
@option('--firewall', '-f',
        is_flag=True,
        help='Setup SSH on a random port and add it to firewall.')
@option('--git_clone_url', '-g',
        metavar='GIT_URL',
        help='personal git URL for your dot files, defaults to '
             'https://github.com/jessebot/dot_files')
@option('--log_level' '-l',
        metavar='LOGLEVEL',
        type=Choice(['debug', 'info', 'warn', 'error']),
        help='Logging level to use with the script (debug, info, warn, error).'
             ' Defaults to error.')
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
@option('--pkg_managers', '-p',
        default=None,
        multiple=True,
        metavar='PKG_MANAGER',
        type=Choice(['brew', 'pip3.10', 'apt', 'snap', 'flatpak']),
        help='Specific [light_steel_blue]PKG_MANAGER[/] to run. Defaults to '
             'only run brew, pip3.10, & ([i]if linux[/]) apt/snap/flatpak.'
             ' Accepts multiple package managers.\n'
             'Ex: -p [cornflower_blue]brew[/] -p [cornflower_blue]apt')
@option('--pkg_groups', '-e',
        metavar='PKG_GROUP',
        multiple=True,
        type=Choice(['default', 'gaming', 'devops']),
        help='Extra package groups to install. Accepts multiple groups.\n'
             'Ex: -e [cornflower_blue]devops[/] -e [cornflower_blue]gaming')
@option('--remote_host', '-H',
        multiple=True,
        metavar="IP_ADDRESS",
        default=None,
        help='Setup SSH on a random port and add [cornflower_blue]IP_ADDRESS'
             '[/] to firewall')
@option('--silent', '-s',
        is_flag=True,
        help='[i]Experimental[/i]. Do no output anything to the console. (can '
             'still output to file.)')
def main(browser: bool = False,
         delete_existing: bool = False,
         firewall: bool = False,
         git_clone_url: str = "",
         log_level: str = "",
         only_steps: str = "",
         pkg_managers: str = "",
         pkg_groups: str = "",
         remote_host: str = "",
         silent: bool = False):
    """
    Uses config in the script repo in config/packages.yml and config/config.yml
    If run with no options on Linux, it will install brew, pip3.10, apt,
    flatpak, and snap packages. On mac, it only installs brew/pip3.10 packages.
    config loading tries to load: cli options and then .config/onboardme/*
    """

    # before we do anything, we need to make sure this OS is supported
    confirm_os_supported()

    # then process any local user config files in ~/.config/onboardme
    user_prefs = process_user_config(delete_existing, git_clone_url, log_level,
                                     only_steps, pkg_managers, pkg_groups,
                                     silent, remote_host)

    # for console AND file logging
    if not log_level:
        log_level = "info"
    logging.basicConfig(level=log_level.upper, format=FORMAT,
                        datefmt="[%X]", handlers=[RichHandler()])
    global log
    log = logging.getLogger("rich")

    # figure out which steps to run:
    steps = process_steps(only_steps, firewall, browser)

    if 'dot_files' in steps:
        delete_existing = user_prefs['dot_files'].get('delete_existing')
        git_clone_url = user_prefs['dot_files'].get('git_clone_url')
        # this creates a live git repo out of your home directory
        setup_dot_files(OS, delete_existing, git_clone_url)

    if 'font_installation' in steps:
        install_fonts()

    if 'install_pkgs' in steps:
        # these are the package managers we'll be running e.g. brew, pip, etc
        installers = user_prefs['pkg_managers'].get('enabled', [])
        # process additional package lists, if any, such as "gaming" packages
        pkg_groups = user_prefs['pkg_managers'].get('pkg_groups', [])
        run_pkg_mngrs(installers, set(pkg_groups))

    if 'firewall_setup' in steps:
        if remote_host:
            configure_firewall(remote_host)

    if 'vim_setup' in steps:
        # this installs the vim plugins
        vim_setup()

    if 'groups_setup' in steps:
        # will add your user to docker group
        setup_nix_groups()

    print_manual_steps()


if __name__ == '__main__':
    main()
