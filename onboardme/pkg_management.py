import logging as log
from os import path
import shutil

from .constants import OS, PWD, XDG_CONFIG_DIR, HOME_DIR
from .console_logging import print_header
from .console_logging import print_sub_header as sub_header
from .env_config import load_cfg
from .subproc import subproc


def load_packages_config() -> dict:
    """
    Checks if user has local config file before procceding with default config
    """
    # check to make sure the user didn't pass in their own packages.yaml
    usr_pkg_config = path.join(XDG_CONFIG_DIR, 'packages.yaml')
    if path.exists(usr_pkg_config):
        return load_cfg(usr_pkg_config)
    else:
        default_config = path.join(PWD, 'config/packages.yaml')
        return load_cfg(default_config)


def rotate_github_ssh_keys() -> None:
    """
    update SSH pub keys for github.com
    """
    log.info("Rotating github.com ssh keys, just in case...")
    # deletes all keys starting with github.com from ~/.ssh/known_hosts
    subproc(["ssh-keygen -R github.com"])

    # gets the new public keys from github.com
    github_keys = subproc(["ssh-keyscan github.com"])

    # the new github.com keys are not automatically added :( so we do it here
    with open(path.join(HOME_DIR, '.ssh/known_hosts'), 'a') as known_hosts:
        for line in github_keys.split('/n'):
            known_hosts.write(line)


def run_preinstall_cmds(cmd_list: list, pkg_groups: list) -> None:
    """
    takes a list of package manager pre-install commands and runs them
    if second list of package groups contains gaming, runs additional commands
    returns True
    """
    run_gaming_setup = False
    if 'gaming' in pkg_groups:
        run_gaming_setup = True

    for pre_cmd in ['setup', 'update', 'upgrade']:
        if pre_cmd in cmd_list:
            if pre_cmd == 'update' and 'apt' in pre_cmd:
                if run_gaming_setup:
                    log.debug("Run gaming commands to update /etc/apt/sources")
                    cmds = ["sudo dpkg --add-architecture i386",
                            f"sudo {PWD}/scripts/update_apt_sources.sh"]
                    subproc(cmds, spinner=False)

            SPINNER = True
            if 'sudo' in cmd_list[pre_cmd]:
                SPINNER = False

            subproc([cmd_list[pre_cmd]], spinner=SPINNER)
            sub_header(f"[b]{pre_cmd.title()}[/b] completed.")


def run_pkg_mngrs(pkg_mngrs: list, pkg_groups=[]) -> None:
    """
    Installs brew and pip3.11 packages. Also apt, snap, and flatpak on Linux.
    Takes optional variables:
      - pkg_groups: list of optional package groups
      - pkg_mngrs: list of package managers to run
    Returns True
    """
    log.debug(f"passed in pkg_mngrs: {pkg_mngrs}\npkg_groups: {pkg_groups}")

    rotate_github_ssh_keys()

    pkg_mngrs_list_of_dicts = load_packages_config()
    # we iterate through pkg_mngrs which should already be sorted
    for pkg_mngr in pkg_mngrs:
        pkg_mngr_dict = pkg_mngrs_list_of_dicts[pkg_mngr]

        available_pkg_groups = pkg_mngr_dict['packages']
        log.debug(f"pkg groups for {pkg_mngr} are {available_pkg_groups}")

        # brew has a special flow because it works on both linux and mac
        if pkg_mngr == 'brew':
            if 'Darwin' in OS:
                if 'default' in pkg_groups:
                    if type(pkg_groups) is tuple:
                        pkg_groups = list(pkg_groups)
                    pkg_groups.append("macOS")

        # make sure that the package manager has any groups that were passed in
        if any(check in pkg_groups for check in available_pkg_groups):

            pkg_emoji = pkg_mngr_dict['emoji']
            msg = f'{pkg_emoji} [grn][b]{pkg_mngr}[/b][/grn] app management'
            print_header(msg)

            # commands for listing, installing, updating, upgrading, & cleanup
            pkg_cmds = pkg_mngr_dict['commands']

            if pkg_mngr == 'snap' and not shutil.which('snap'):
                log.warn("snap is either not installed, or you need to log out"
                         "and back in (or reboot) for it to be available. "
                         "https://snapcraft.io/docs/installing-snap-on-debian")
                # continues onto the next package manager
                continue

            if pkg_mngr == 'brew':
                # this installs macOS brew taps
                install_brew_taps(pkg_mngr_dict['taps']['macOS'])

            # run package manager specific setup if needed: update/upgrade
            run_preinstall_cmds(pkg_cmds, pkg_groups)

            # run the list command for the given package manager
            list_cmd = pkg_cmds['list']
            # TODO: figure out a way to make this less hacky
            if pkg_mngr == 'apt':
                list_cmd = path.join(PWD, list_cmd)
            list_pkgs = subproc([list_cmd], quiet=True)

            if list_pkgs:
                # create list of installed packages to iterate on
                installed_pkgs = list_pkgs.split()
            else:
                installed_pkgs = []

            # iterate through package groups for a given package manager
            for pkg_group in pkg_groups:
                # if package group is in the packages.yaml file
                if pkg_group in available_pkg_groups:
                    if pkg_group == "macOS":
                        # zathura needs some help on macOS
                        check_zathura()

                    install_pkg_group(pkg_cmds['install'],
                                      available_pkg_groups[pkg_group],
                                      installed_pkgs)
                    sub_header(f'{pkg_group.title()} packages installed.')

            # run final cleanup commands, if any
            if 'cleanup' in pkg_cmds:
                subproc([pkg_cmds['cleanup']])
                sub_header("[b]Cleanup[/b] step Completed.")


def install_pkg_group(install_cmd: str, pkgs_to_install: list,
                      installed_pkgs: list) -> None:
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


def install_brew_taps(taps: list) -> None:
    """
    Checks current brew taps, and then runs brew tap {tap} on any taps that are
    in a list of git repos from packages.yaml, and aren't already tapped
    """
    current_taps = subproc(["brew tap"]).split('\n')
    log.debug(f"taps list is: {taps}")
    log.debug(f"Current taps are: {current_taps}")

    # for each tap, complete cmd by prepending `brew tap`
    for index, tap in enumerate(taps):
        log.debug(f"index: {index} tap: {tap}")
        # only brew tap if they don't already exist
        if tap not in current_taps:
            subproc(["brew tap " + tap])


def check_zathura() -> None:
    """
    make sure zathura is installed on macos
    installs via brew if it's not installed
    always returns True if everything was successful
    """
    if not shutil.which("zathura"):
        zathura_pdf = "$(brew --prefix zathura-pdf-mupdf)"
        cmds = ["mkdir -p $(brew --prefix zathura)/lib/zathura",
                f"ln -s {zathura_pdf}/libpdf-mupdf.dylib" +
                f"{zathura_pdf}/lib/zathura/libpdf-mupdf.dylib"]
        subproc(cmds, quiet=True)
