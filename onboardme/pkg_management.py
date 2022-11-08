#!/usr/bin/env python3.10
import logging as log
from os import path

# custom libs
from .env_config import OS, PWD, load_yaml
from .console_logging import print_header, print_msg
from .console_logging import print_sub_header as sub_header
from .subproc import subproc


def brew_install_upgrade(package_groups=['default']):
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

    if 'default' in package_groups:
        subproc(['brew update --quiet',
                 'brew upgrade --quiet',
                 f'{install_cmd} --global'])

    # install os specific or package group specific brew stuff
    brewfile = path.join(PWD, 'config/brew/Brewfile_')

    # sometimes there isn't an OS specific brewfile, but there always is 4 mac
    os_brewfile = path.exists(brewfile + OS[0])

    if os_brewfile or package_groups:
        install_cmd += f" --file={brewfile}"

        if os_brewfile:
            os_msg = f'[b]{OS[0]}[/b] specific package installs...'
            sub_header(os_msg)
            subproc([f'{install_cmd}{OS[0]}'], error_ok=True)
            print_msg(f'{OS[0]} specific packages installed.')

        if package_groups:
            for group in package_groups:
                group_file = brewfile + group
                if group != "default" and path.exists(group_file):
                    # Installing devops specific brew app Installs/Upgrades
                    msg = f"{group.title()} specific package installs..."
                    sub_header(msg)
                    subproc([f'{install_cmd}{group}'], error_ok=True)
                    print_msg(f'{group.title()} specific packages installed.')

    # cleanup operation doesn't seem to happen automagically :shrug:
    sub_header('[b]brew[/b] final cleanup')
    subproc(['brew cleanup'])
    print_msg('Cleanup completed.')
    return


def run_pkg_mngrs(pkg_mngrs=[], pkg_groups=[]):
    """
    Installs packages with apt, brew, pip3.10, snap, flatpak. If no pkg_mngrs
    list passed in, only use brew/pip3.10 for mac. Takes optional variable,
    pkg_group_lists to install optional packages.
    Returns True.
    """
    pkg_mngrs_list_of_dicts = load_yaml(path.join(PWD, 'config/packages.yml'))
    log.debug(f"pkg_mngrs: {pkg_mngrs}", extra={"markup": True})
    log.debug(f"pkg_groups: {pkg_groups}", extra={"markup": True})

    # we iterate through pkg_mngrs which should already be sorted
    for pkg_mngr in pkg_mngrs:

        # brew has a special flow with "Brewfile"s
        if pkg_mngr == 'brew':
            if any(check in pkg_groups for check in ['devops', 'default']):
                brew_install_upgrade(pkg_groups)
            # skip everything below because install process already covered
            continue

        pkg_mngr_dict = pkg_mngrs_list_of_dicts[pkg_mngr]
        required_pkg_groups = pkg_mngr_dict['packages']

        debug_line = f"pkg groups for {pkg_mngr} are {required_pkg_groups}"
        log.debug(debug_line, extra={"markup": True})

        # make sure that the package manage has any groups that were passed in
        if any(check in pkg_groups for check in required_pkg_groups):

            pkg_emoji = pkg_mngr_dict['emoji']
            msg = f'{pkg_emoji} [green][b]{pkg_mngr}[/b][/] app Installs'
            print_header(msg)
            print('')

            # run package manager specific setup if needed, & updates/upgrades
            pkg_cmds = pkg_mngr_dict['commands']
            log.debug(f"package manager commands are: {pkg_cmds}")
            for pre_cmd in ['setup', 'update', 'upgrade']:
                if pre_cmd in pkg_cmds:
                    SPINNER = True
                    if 'sudo' in pkg_cmds[pre_cmd]:
                        SPINNER = False
                    subproc([pkg_cmds[pre_cmd]], spinner=SPINNER)
                    sub_header(f"[b]{pre_cmd.title()}[/b] completed.")

            # list of actually installed packages
            installed_pkgs = subproc([pkg_cmds['list']], quiet=True)

            for pkg_group in pkg_groups:
                if pkg_group in required_pkg_groups:
                    install_pkg_group(installed_pkgs,
                                      required_pkg_groups[pkg_group],
                                      pkg_cmds['install'])

                    sub_header(f'{pkg_group.title()} packages installed.')

            if 'cleanup' in pkg_cmds:
                subproc([pkg_cmds['cleanup']])
                sub_header("[b]Cleanup[/b] step Completed.")
    return


def install_pkg_group(installed_pkgs=[], pkgs_to_install=[], install_cmd=""):
    """
    installs packages if they are not already intalled with intall_cmd
    Returns True.
    """
    SPINNER = True
    install_pkg = False
    # the spinner status thing rich provides breaks with input
    if 'sudo' in install_cmd:
        SPINNER = False

    if 'upgrade' in install_cmd or not installed_pkgs:
        install_pkg = True

    log.debug(f"pkgs_to_install are {pkgs_to_install}",
              extra={"markup": True})
    for pkg in pkgs_to_install:
        if installed_pkgs:
            if pkg not in installed_pkgs:
                install_pkg = True
        if install_pkg:
            subproc([install_cmd + pkg], quiet=True, spinner=SPINNER)
    return True
