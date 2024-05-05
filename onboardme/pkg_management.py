import logging as log
from os import path
from pathlib import Path
import shutil

from .constants import OS, PWD, HOME_DIR, load_cfg
from .console_logging import print_header
from .console_logging import print_sub_header as sub_header
from .subproc import subproc


def rotate_github_ssh_keys() -> None:
    """
    update SSH pub keys for github.com
    """
    log.info("Rotating github.com ssh keys, just in case...")

    # create directory if it doesn't exist
    ssh_dir = path.join(HOME_DIR, '.ssh')
    if not path.exists(ssh_dir):
        Path(ssh_dir).mkdir(exist_ok=True)

    # create file if it doesn't exist
    known_hosts_file = path.join(ssh_dir, 'known_hosts')
    if not path.exists(ssh_dir):
        subproc([f"touch {known_hosts_file}"])

    # deletes all keys starting with github.com from ~/.ssh/known_hosts
    subproc(["ssh-keygen -R github.com"])

    # gets the new public keys from github.com
    github_keys = subproc(["ssh-keyscan github.com"])

    # the new github.com keys are not automatically added :( so we do it here
    with open(known_hosts_file, 'a') as known_hosts:
        for line in github_keys.split('/n'):
            known_hosts.write(line)


def run_preinstall_cmds(cmd_list: list,
                        pkg_groups: list,
                        no_upgrade: bool) -> None:
    """
    takes a list of package manager pre-install commands and runs them
    if second list of package groups contains gaming, runs additional commands
    returns True
    """
    run_gaming_setup = False
    if 'gaming' in pkg_groups:
        run_gaming_setup = True

    pre_cmds = ['setup', 'update', 'upgrade']

    if no_upgrade:
        pre_cmds.pop(2)

    for pre_cmd in pre_cmds:
        if pre_cmd in cmd_list:
            if pre_cmd == 'update' and 'apt' in cmd_list[pre_cmd]:
                if run_gaming_setup:
                    log.debug("Run gaming commands to update /etc/apt/sources")
                    cmds = ["sudo dpkg --add-architecture i386",
                            f"sudo {PWD}/scripts/update_apt_sources.sh"]
                    subproc(cmds, spinner=False)
            if pre_cmd == 'upgrade' and 'brew' in cmd_list[pre_cmd]:
                if OS[0] == 'Darwin':
                    log.debug("we'll run upgrade --cask for macOS")
                    subproc(["brew upgrade --cask"])

            SPINNER = True
            if 'sudo' in cmd_list[pre_cmd]:
                SPINNER = False

            subproc([cmd_list[pre_cmd]], spinner=SPINNER)
            sub_header(f"[b]{pre_cmd.title()}[/b] completed.")


def run_pkg_mngrs(pkg_mngrs: list, pkg_groups: list = [], no_upgrade: bool = False) -> None:
    """
    Installs brew, pip3.12/pip3.11, and pipx packages on both Debian/Ubuntu/macOS
    Also apt, snap, and flatpak on Linux. Takes optional variables:
      - pkg_groups: list of optional package groups
      - pkg_mngrs: list of package managers to run
    Returns True
    """
    log.debug(f"passed in pkg_mngrs: {pkg_mngrs}\npkg_groups: {pkg_groups}")

    rotate_github_ssh_keys()

    pkg_mngrs_list_of_dicts = load_cfg('packages.yml')
    # we iterate through pkg_mngrs which should already be sorted
    for pkg_mngr in pkg_mngrs:
        pkg_mngr_dict = pkg_mngrs_list_of_dicts[pkg_mngr]

        available_pkg_groups = pkg_mngr_dict['packages']
        log.debug(f"pkg groups for {pkg_mngr} are {available_pkg_groups}")

        # brew has a special flow because it works on both linux and mac
        if pkg_mngr == 'brew':
            if 'Darwin' in OS:
                if 'default' in pkg_groups:
                    if isinstance(pkg_groups, tuple):
                        pkg_groups = list(pkg_groups)
                    pkg_groups.append("macOS")

        # make sure that the package manager has any groups that were passed in
        if any(check in pkg_groups for check in available_pkg_groups):

            pkg_emoji = pkg_mngr_dict['emoji']
            msg = f'{pkg_emoji} [grn][b]{pkg_mngr}[/b][/grn] app management'
            print_header(msg)

            # commands for listing, installing, updating, upgrading, & cleanup
            pkg_cmds = pkg_mngr_dict['commands']

            # make sure we use any required env vars during installs
            install_env_vars = pkg_mngr_dict.get('env_vars', None)

            if pkg_mngr == 'snap' and not shutil.which('snap'):
                log.warn("snap is either not installed, or you need to log out"
                         "and back in (or reboot) for it to be available. "
                         "https://snapcraft.io/docs/installing-snap-on-debian")
                # continues onto the next package manager
                continue

            if pkg_mngr == 'flatpak' and not shutil.which('flatpak'):
                log.warn("flatpak is either not installed, or you need to log out"
                         "and back in (or reboot) for it to be available. "
                         "https://flatpak.org/setup/")
                # continues onto the next package manager
                continue

            if pkg_mngr == 'pip3.11' and not shutil.which('pip3.11'):
                log.info("pip3.11 is either not installed, or you need to log out"
                         "and back in for it to be available.")
                # continues onto the next package manager
                continue

            # run package manager specific setup if needed: update/upgrade
            run_preinstall_cmds(pkg_cmds, pkg_groups, no_upgrade)

            # run the list command for the given package manager
            installed_pkgs = []
            list_cmd = pkg_cmds.get('list', None)
            if list_cmd:
                list_pkgs = subproc([list_cmd], quiet=True)
                if list_pkgs:
                    # create list of installed packages to iterate on
                    installed_pkgs = list_pkgs.split()

            # iterate through package groups for a given package manager
            for pkg_group in pkg_groups:
                # if package group is in the packages.yaml file
                if pkg_group in available_pkg_groups:
                    # for zathura, a document viewer, might delete
                    # if pkg_group == "macOS":
                    #     # zathura needs some help on macOS
                    #     check_zathura()
                    install_pkg_group(pkg_cmds['install'],
                                      available_pkg_groups[pkg_group],
                                      installed_pkgs,
                                      install_env_vars,
                                      no_upgrade)
                    sub_header(f'{pkg_group.title()} packages installed.')

            # run final cleanup commands, if any
            if 'cleanup' in pkg_cmds:
                subproc([pkg_cmds['cleanup']])
                sub_header("[b]Cleanup[/b] step Completed.")


def install_pkg_group(install_cmd: str,
                      pkgs_to_install: list,
                      installed_pkgs: list,
                      install_env_vars: dict,
                      no_upgrade: bool
                      ) -> None:
    """
    Installs packages if they are not already installed.
    provided install command string.
    Returns True.
    """
    log.debug(f"Currently installed packages: {installed_pkgs}")
    log.info(f"Packages to install are: {pkgs_to_install}")

    # apt is smart enough to install everything at once correctly
    if 'apt' in install_cmd:
        all_packages = ' '.join(pkgs_to_install)
        subproc([install_cmd + all_packages], quiet=True, env=install_env_vars)
        return

    # this installs packages one by one
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
                if no_upgrade or 'upgrade' not in install_cmd:
                    log.info(f"{pkg} already installed. Moving on.")
                    # continues to the next pkg in the pkgs_to_install list
                    continue
                # if the install command has upgrade in it, we always run it
                else:
                    log.info(f"Upgrading {pkg} now...")

        # Actual installation
        subproc([install_cmd + pkg], quiet=True, env=install_env_vars)


# not currently using zathura on macOS, so removing as it's untested
# def check_zathura() -> None:
#     """
#     make sure zathura is installed on macos
#     installs via brew if it's not installed
#     always returns True if everything was successful
#     """
#     if not shutil.which("zathura"):
#         zathura_pdf = "$(brew --prefix zathura-pdf-mupdf)"
#         cmds = ["mkdir -p $(brew --prefix zathura)/lib/zathura",
#                 f"ln -s {zathura_pdf}/libpdf-mupdf.dylib" +
#                 f"{zathura_pdf}/lib/zathura/libpdf-mupdf.dylib"]
#         subproc(cmds, quiet=True)
