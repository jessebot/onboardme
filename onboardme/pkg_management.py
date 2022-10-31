#!/usr/bin/env python3.10
from os import getenv, path, uname
# rich helps pretty print everything
import yaml

# custom libs
from .console_logging import print_header, print_msg
from .subproc import subproc


PWD = path.dirname(__file__)
with open(f'{PWD}/config/config.yml', 'r') as yaml_file:
    OPTS = yaml.safe_load(yaml_file)

# user env info
HOME_DIR = getenv("HOME")
# run uname to get operating system and hardware info
SYSINFO = uname()
# this will be something like Darwin_x86_64
OS = f"{SYSINFO.sysname}_{SYSINFO.machine}"


def brew_install_upgrade(OS="Darwin", package_groups=['default']):
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

    # install os specific or package group specific brew stuff
    brewfile = path.join(PWD, 'config/brew/Brewfile_')
    # sometimes there isn't an OS specific brewfile, but there always is 4 mac
    os_brewfile = path.exists(brewfile + OS)
    if os_brewfile or package_groups:
        install_cmd += f" --file={brewfile}"

        if os_brewfile:
            os_msg = f'[i][dim][b]{OS}[/b] specific ' + brew_msg
            print_msg(os_msg)
            subproc([f'{install_cmd}{OS}'], True)

        if package_groups:
            for group in package_groups:
                if group != "default":
                    msg = group.title + ' specific ' + brew_msg
                    print_header(msg)
                    subproc([f'{install_cmd}{group}'], True)

    # cleanup operation doesn't seem to happen automagically :shrug:
    cleanup_msg = '[i][dim]🍺 [green][b]brew[/b][/] final upgrade/cleanup'
    print_msg(cleanup_msg)
    subproc(['brew cleanup'])

    print_msg('[dim][i]Completed.')
    return


def run_pkg_mngrs(pkg_mngrs=[], pkg_groups=[]):
    """
    Installs packages with apt, brew, pip3.10, snap, flatpak. If no pkg_mngrs
    list passed in, only use brew/pip3.10 for mac. Takes optional variable,
    pkg_group_lists to install optional packages.
    """
    # brew has a special flow with brew files
    if 'brew' in pkg_mngrs:
        brew_install_upgrade(SYSINFO.sysname, pkg_groups)
        pkg_mngrs.remove('brew')

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
                subproc([pkg_cmds[pre_cmd]], False, False, False)

        # list of actually installed packages
        installed_pkgs = subproc([pkg_cmds['list']], False, True)
        # list of SHOULD BE installed packages
        required_pkgs = pkg_mngr_dict['packages']

        # iterate through package groups, such as: default, gaming, devops...
        for pkg_group in pkg_groups:
            if required_pkgs[pkg_group]:
                if pkg_group != 'default':
                    msg = (f"Installing {pkg_group.replace('_', ' ')} "
                           f"{pkg_emoji} [b]{pkg_mngr}[/b] packages")
                    print_header(msg, "cornflower_blue")

                spinner = True
                if 'sudo' in  pkg_cmds['install']:
                    spinner = False
                for pkg in required_pkgs[pkg_group]:
                    install_cmd = pkg_cmds['install'] + pkg
                    if pkg not in installed_pkgs or 'upgrade' in install_cmd:
                        subproc([install_cmd], False, True, spinner)
                print_msg('[dim][i]Completed.')
    return
