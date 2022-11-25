import logging as log
from os import path

# custom libs
from .env_config import OS, PWD, HOME_DIR, load_cfg
from .console_logging import print_header
from .console_logging import print_sub_header as sub_header
from .subproc import subproc


def run_pkg_mngrs(pkg_mngrs=[], pkg_groups=[]):
    """
    Installs brew and pip3.11 packages. Also apt, snap, and flatpak on Linux.
    Takes optional variables:
      - pkg_groups: list of optional package groups
      - pkg_mngrs: list of package managers to run
    Returns True
    """
    # check to make sure the user didn't pass in their own packages.yml
    user_packages = path.join(HOME_DIR, '.config/onboardme/packages.yml')
    if path.exists(user_packages):
        pkg_mngrs_list_of_dicts = load_cfg(user_packages)
    else:
        default_config = path.join(PWD, 'config/packages.yml')
        pkg_mngrs_list_of_dicts = load_cfg(default_config)

    log.debug(f"pkg_mngrs: {pkg_mngrs}")
    log.debug(f"pkg_groups: {pkg_groups}")

    # we iterate through pkg_mngrs which should already be sorted
    for pkg_mngr in pkg_mngrs:

        pkg_mngr_dict = pkg_mngrs_list_of_dicts[pkg_mngr]
        available_pkg_groups = pkg_mngr_dict['packages']

        # brew has a special flow because it works on both linux and mac
        if pkg_mngr == 'brew':
            if 'Darwin' in OS:
                pkg_groups.append("macOS")

        debug_line = f"pkg groups for {pkg_mngr} are {available_pkg_groups}"
        log.debug(debug_line)

        # make sure that the package manage has any groups that were passed in
        if any(check in pkg_groups for check in available_pkg_groups):

            pkg_emoji = pkg_mngr_dict['emoji']
            msg = f'{pkg_emoji} [green][b]{pkg_mngr}[/b][/] app Installs'
            print_header(msg)

            pkg_cmds = pkg_mngr_dict['commands']
            log.debug(f"{pkg_mngr} pre-install commands are: {pkg_cmds}")

            # gaming has a special flow that needs to be done before updates
            if "gaming" in pkg_groups and pkg_mngr == "apt":
                run_gaming_specific_cmds()

            # run package manager specific setup if needed, & updates/upgrades
            for pre_cmd in ['setup', 'update', 'upgrade']:
                if pre_cmd in pkg_cmds:
                    SPINNER = True
                    if 'sudo' in pkg_cmds[pre_cmd]:
                        SPINNER = False
                    subproc([pkg_cmds[pre_cmd]], spinner=SPINNER)
                    sub_header(f"[b]{pre_cmd.title()}[/b] completed.")

            # list of actually installed packages
            installed_pkgs = subproc([pkg_cmds['list']])

            for pkg_group in pkg_groups:
                if pkg_group in available_pkg_groups:

                    install_pkg_group(installed_pkgs,
                                      available_pkg_groups[pkg_group],
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

    log.debug(f"pkgs_to_install are {pkgs_to_install}")

    for pkg in pkgs_to_install:
        if installed_pkgs:
            if pkg not in installed_pkgs:
                log.info(f"{pkg} not in installed packages. Installing...")
                install_pkg = True
        if install_pkg:
            subproc([install_cmd + pkg], quiet=True, spinner=SPINNER)
    return True


def run_gaming_specific_cmds():
    """
    run commands specific to gaming package group:
      add i386 architecture, add contrib/non-free to sources.list, and update
    """
    cmds = ["sudo dpkg --add-architecture i386",
            f"sudo {PWD}/scripts/update_apt_sources.sh"]
    subproc(cmds, spinner=False)
    return True
