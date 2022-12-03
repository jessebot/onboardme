import logging as log
import shutil
from os import path
import shutil

from .env_config import OS, PWD, HOME_DIR, load_cfg
from .console_logging import print_header
from .console_logging import print_sub_header as sub_header
from .subproc import subproc


def run_preinstall_cmds(cmd_list=[], pkg_groups=[]):
    """
    takes a list of package manager pre-install commands and runs them
    if second list of package groups contains gaming, runs additional commands
    returns True
    """
    if 'gaming' in pkg_groups and 'apt' in cmd_list['update']:
        log.debug("Run gaming specific commands to update /etc/apt/sources")
        cmds = ["sudo dpkg --add-architecture i386",
                f"sudo {PWD}/scripts/update_apt_sources.sh"]
        subproc(cmds, spinner=False)

    for pre_cmd in ['setup', 'update', 'upgrade']:
        if pre_cmd in cmd_list:
            SPINNER = True
            if 'sudo' in cmd_list[pre_cmd]:
                SPINNER = False

            subproc([cmd_list[pre_cmd]], spinner=SPINNER)
            sub_header(f"[b]{pre_cmd.title()}[/b] completed.")

    return True


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

    log.debug(f"passed in pkg_mngrs: {pkg_mngrs}")
    log.debug(f"passed in pkg_groups: {pkg_groups}")

    # we iterate through pkg_mngrs which should already be sorted
    for pkg_mngr in pkg_mngrs:

        pkg_mngr_dict = pkg_mngrs_list_of_dicts[pkg_mngr]
        available_pkg_groups = pkg_mngr_dict['packages']

        # brew has a special flow because it works on both linux and mac
        if pkg_mngr == 'brew':
            if 'Darwin' in OS:
                pkg_groups.append("macOS")

        log.debug(f"pkg groups for {pkg_mngr} are {available_pkg_groups}")

        # make sure that the package manager has any groups that were passed in
        if any(check in pkg_groups for check in available_pkg_groups):

            pkg_emoji = pkg_mngr_dict['emoji']
            msg = f'{pkg_emoji} [green][b]{pkg_mngr}[/b][/] app Installs'
            print_header(msg)

            # commands for listing, installing, updating, upgrading, & cleanup
            pkg_cmds = pkg_mngr_dict['commands']

            if pkg_mngr == 'snap' and not shutil.which('snap'):
                # ref: https://snapcraft.io/docs/installing-snap-on-debian
                log.warn("snap is either not installed, or you need to log out"
                         "and back in (or reboot) for it to be available.")
                # continues onto the next package manager
                continue
            else:
                # run package manager specific setup if needed: update/upgrade
                run_preinstall_cmds(pkg_cmds, pkg_groups)

            # run the list command for the given package manager
            list_pkgs = subproc([pkg_cmds['list']], quiet=True)
            # create list of installed packages to iterate on
            installed_pkgs = list_pkgs.split()

            # iterate through package groups for a given package manager
            for pkg_group in pkg_groups:
                # if package group is in the packages.yml file
                if pkg_group in available_pkg_groups:
                    if pkg_group == "macOS":
                        check_zathura()
                    install_pkg_group(pkg_cmds['install'],
                                      available_pkg_groups[pkg_group],
                                      installed_pkgs)
                    sub_header(f'{pkg_group.title()} packages installed.')

            # run final cleanup commands, if any
            if 'cleanup' in pkg_cmds:
                subproc([pkg_cmds['cleanup']])
                sub_header("[b]Cleanup[/b] step Completed.")
    return True


def install_pkg_group(install_cmd="", pkgs_to_install=[], installed_pkgs=[]):
    """
    Installs packages if they are not already installed.
    provided install command string.
    Returns True.
    """
    log.debug(f"Currently installed packages: {installed_pkgs}")
    log.info(f"Packages to install are: {pkgs_to_install}")

    for pkg in pkgs_to_install:
        if not installed_pkgs:
            log.info(f"{pkg} isn't installed. Installing now...")
        else:
            # this variable defaults to pkg unless it has special strings in it
            pkg_short_name = pkg

            # for things like steam:i386 for apt
            if ":" in pkg:
                pkg_short_name = pkg.split(':')[0]

            # this covers things like "--cask iterm2" for brew
            if "--cask" in pkg:
                pkg_short_name = pkg.split(' ')[1]

            log.debug(f"Checking if {pkg_short_name} is installed...")
            if pkg_short_name in installed_pkgs:
                if 'upgrade' not in install_cmd:
                    log.info(f"{pkg} already installed. Moving on.")
                    # continues to the next pkg in the pkgs_to_install list
                    continue
                # if the install command has upgrade in it, we always run it
                else:
                    log.info(f"Upgrading {pkg} now...")

        # Actual installation
        subproc([install_cmd + pkg], quiet=True)
    return True


def check_zathura():
    """
    make sure zathura is installed on macos
    installs via brew if it's not installed
    always returns True if everything was successful
    """
    if not shutil.which("zathura"):
        zathura_pdf = "$(brew --prefix zathura-pdf-mupdf)"
        cmds = ["brew tap zegervdv/zathura",
                "brew install zathura",
                "brew install zathura-pdf-mupdf",
                "mkdir -p $(brew --prefix zathura)/lib/zathura",
                f"ln -s {zathura_pdf}/libpdf-mupdf.dylib" +
                f"{zathura_pdf}/lib/zathura/libpdf-mupdf.dylib"]
        subproc(cmds, quiet=True)
    return True
