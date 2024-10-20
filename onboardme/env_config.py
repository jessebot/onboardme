"""
config variable processing library for onboardme
"""

import logging as log

# rich helps pretty print everything
from rich.prompt import Confirm

# custom libs
from .constants import OS, USR_CONFIG_FILE, DEFAULT_PKG_GROUPS, HOME_DIR
from .console_logging import print_panel


def check_os_support() -> None:
    """
    verify we're on a supported OS and ask to quit if not.
    """
    if OS[0] not in ('Linux', 'Darwin'):
        msg = (f"[ohno]{OS}[/ohno] isn't officially supported. We"
               " have only tested Debian, Ubuntu, and macOS.")
        print_panel(msg, "⚠️  [warn]WARNING")

        quit_y = Confirm.ask("🌊 You're in uncharted waters. Wanna quit?")
        if quit_y:
            print_panel("That's probably safer. Have a safe day, friend.",
                        "Safety Award ☆ ")
            quit()
        else:
            print_panel("[red]Yeehaw, I guess.", "¯\\_(ツ)_/¯")
    else:
        print_panel("Operating System and Architechure [green]supported ♥",
                    "[cornflower_blue]Compatibility Check")


def process_steps(steps: list, firewall: bool = False, browser: bool = False) -> list:
    """
    process which steps to run for which OS, which steps the user passed in,
    and then make sure dependent steps are always run.

    Returns a list of str type steps to run.

    # TODO: if 'capslock_to_control' in steps: map_caps_to_control()
    """
    if steps:
        steps_list = list(steps)
        # setting up neovim is useless if we don't have an init.vim or init.lua
        if 'neovim_setup' in steps_list and 'dot_files' not in steps_list:
            steps_list.append('dot_files')

        # need cron files to setup crontabs
        if 'cron' in steps_list and 'dot_files' not in steps_list:
            steps_list.append('dot_files')

        if firewall and 'Linux' in OS:
            # currently don't have a great firewall on macOS, sans lulu
            steps_list.append('firewall_setup')

    removed_duplicates = set(steps_list)
    steps = list(removed_duplicates)
    default_order = ['dot_files', 'packages', 'cron', 'font_setup', 'neovim_setup']
    if OS[0] == 'Linux':
        default_order.append('group_setup')
    else:
        default_order.append('sudo_setup')

    # Rearrange list by other list order Using list comprehension
    return [ele for ele in default_order if ele in steps]


def sort_pkgmngrs(package_managers_list: list) -> list:
    """
    make sure the package managers are in the right order 🤦
    e.g. apt installs snap and flatpak, so niether can be run until apt is run

    Takes list of package manager str and reorders them be (if they exist):
       ['brew', 'pip3.12', 'pip3.11', 'pipx', 'apt', 'snap', 'flatpak']
    """
    pkg_mngr_default_order = ['brew', 'pip3.12', 'pip3.11', 'pipx', 'apt', 'snap', 'flatpak']

    # Rearrange list by other list order Using list comprehension
    return [ele for ele in pkg_mngr_default_order if ele in package_managers_list]


def fill_in_defaults(defaults: dict, user_config: dict,
                     always_prefer_default=False) -> dict:
    """
    Compares/Combines a default dict and another dict. Prefer default values
    only if the value is empty in the second dict. Then return new dict.
    """
    for key, value in user_config.items():
        # we have to iterate through the entire config file, and who knows how
        # many levels there are, so we use recursion of this function
        if isinstance(value, dict):
            result_config = fill_in_defaults(defaults[key], user_config[key],
                                             always_prefer_default)
            user_config[key] = result_config

        if not value or always_prefer_default:
            user_config[key] = defaults[key]

    return user_config


def process_configs(overwrite: bool,
                    repo: str,
                    git_branch: str,
                    git_config_dir: str,
                    pkg_mngrs: list,
                    pkg_groups: list,
                    firewall: bool,
                    remote_host: str,
                    steps: list,
                    log_file: str,
                    log_level: str) -> dict:
    """
    process the config in ~/.config/onboardme/config.yml if it exists,
    then process the cli dict, and fill in defaults for anything not explicitly
    defined. Returns full final config as dict for use in script.
    """
    if remote_host:
        firewall = True
        if isinstance(remote_host, str):
            remote_host = [remote_host]

    if "~" in git_config_dir:
        git_config_dir = git_config_dir.replace("~", HOME_DIR)

    cli_dict = {'package': {'managers': {OS[0]: pkg_mngrs},
                            'groups': pkg_groups},
                'log': {'file': log_file, 'level': log_level},
                'remote_hosts': remote_host,
                'firewall': firewall,
                'steps': {OS[0]: steps},
                'dot_files': {'overwrite': overwrite,
                              'git_url': repo,
                              'git_branch': git_branch,
                              'git_config_dir': git_config_dir}}

    log.debug(f"cli_dict is:\n{cli_dict}\n")

    if OS[0] == 'Darwin':
        try:
            USR_CONFIG_FILE['package']['managers'].pop('Linux')
            USR_CONFIG_FILE['steps'].pop('Linux')
        except KeyError:
            pass
    else:
        try:
            USR_CONFIG_FILE['package']['managers'].pop('Darwin')
            USR_CONFIG_FILE['steps'].pop('Darwin')
        except KeyError:
            pass

    USR_CONFIG_FILE['package']['groups'] = DEFAULT_PKG_GROUPS
    log.debug(f"🗂 ⚙️  user_config_file: \n{USR_CONFIG_FILE}\n")
    final_defaults = fill_in_defaults(cli_dict, USR_CONFIG_FILE, True)

    log.debug(" final config after filling cli_dict in with defaults:\n"
              f"{final_defaults}\n")

    # make sure the steps are in a valid order
    valid_steps = process_steps(final_defaults['steps'][OS[0]],
                                final_defaults.get('remote_hosts', False))
    final_defaults['steps'][OS[0]] = valid_steps

    # make sure the package managers are in a valid order
    sorted_mngrs = sort_pkgmngrs(final_defaults['package']['managers'][OS[0]])
    final_defaults['package']['managers'][OS[0]] = sorted_mngrs

    return final_defaults
