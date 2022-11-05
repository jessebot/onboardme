#!/usr/bin/env python3.10
import logging as log
from os import path

# custom libs
from .env_config import OS, PWD, load_yaml
from .console_logging import print_header, print_msg
from .subproc import subproc


def brew_install_upgrade(os="Darwin", package_groups=['default']):
    """
    Run the install/upgrade of packages managed by brew, also updates brew
    Always installs the .Brewfile (which has libs that work on both mac/linux)
    Accepts args:
        * os     - string arg of either Darwin or Linux
        * devops - bool, installs devops brewfile, defaults to false
    """
    brew_msg = '[green][b]brew[/b][/] app Installs/Upgrades'
    print_header('🍺 ' + brew_msg)

    install_cmd = "brew bundle --quiet"

    subproc(['brew update --quiet', 'brew upgrade --quiet',
             f'{install_cmd} --global'])

    # install os specific or package group specific brew stuff
    brewfile = path.join(PWD, 'config/brew/Brewfile_')
    # sometimes there isn't an OS specific brewfile, but there always is 4 mac
    os_brewfile = path.exists(brewfile + os)
    if os_brewfile or package_groups:
        install_cmd += f" --file={brewfile}"

        if os_brewfile:
            os_msg = f'[i][dim][b]{os}[/b] specific ' + brew_msg
            print_msg(os_msg)
            subproc([f'{install_cmd}{os}'], error_ok=True)

        if package_groups:
            for group in package_groups:
                group_file = brewfile + group
                if group != "default" and os.path.exists(group_file):
                    msg = group.title + ' specific ' + brew_msg
                    print_header(msg)
                    subproc([f'{install_cmd}{group}'], error_ok=True)

    # cleanup operation doesn't seem to happen automagically :shrug:
    cleanup_msg = '[i][dim][green][b]brew[/b][/] final upgrade/cleanup'
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
    pkg_mngrs_list_of_dicts = load_yaml(path.join(PWD, 'config/packages.yml'))
    log.debug(f"pkg_mngrs: {pkg_mngrs}", extra={"markup": True})

    # we iterate through pkg_mngrs which should already be sorted
    for pkg_mngr in pkg_mngrs:
        # brew has a special flow with "Brewfile"s
        if pkg_mngr == 'brew':
            brew_install_upgrade(OS[0], pkg_groups)
            continue
        pkg_mngr_dict = pkg_mngrs_list_of_dicts[pkg_mngr]
        pkg_emoji = pkg_mngr_dict['emoji']
        msg = f'{pkg_emoji} [green][b]{pkg_mngr}[/b][/] app Installs'
        print_header(msg)

        # run package manager specific setup if needed, and updates/upgrades
        pkg_cmds = pkg_mngr_dict['commands']
        for pre_cmd in ['setup', 'update', 'upgrade']:
            if pre_cmd in pkg_cmds:
                subproc([pkg_cmds[pre_cmd]], spinner=False)

        # list of actually installed packages
        installed_pkgs = subproc([pkg_cmds['list']], quiet=True)
        # list of SHOULD BE installed packages
        required_pkgs = pkg_mngr_dict['packages']

        for pkg_group in pkg_groups:
            if required_pkgs[pkg_group]:
                if pkg_group != 'default':
                    msg = (f"Installing {pkg_group.replace('_', ' ')} "
                           f"{pkg_emoji} [b]{pkg_mngr}[/b] packages")
                    print_header(msg, "cornflower_blue")

                install_pkg_group(installed_pkgs, required_pkgs[pkg_group],
                                  pkg_cmds['install'])
    return


def install_pkg_group(installed_pkgs=[], pkgs_to_install=[], install_cmd=""):
    """
    installs packages if they are not already intalled with intall_cmd
    """
    install_pkg = False
    spinner = True
    # the spinner status thing rich provides breaks with input
    if 'sudo' in install_cmd:
        spinner = False

    if 'upgrade' in install_cmd:
        install_pkg = True

    for pkg in pkgs_to_install:
        if installed_pkgs:
            if pkg in installed_pkgs:
                install_pkg = True
        if install_pkg:
            subproc([install_cmd + pkg], quiet=True, spinner=spinner)
    print_msg('[dim][i]Completed.')

    return
