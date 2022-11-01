#!/usr/bin/env python3.10
# Onboarding script for macOS and Debian by jessebot@Linux.com
import logging
from os import getenv, path, uname
# rich helps pretty print everything
from rich.prompt import Confirm
from rich.logging import RichHandler
from .console_logging import print_panel
import yaml
# this is the only logger that needs to updated manually if you are
# troubleshooting. set to logging.DEBUG to see errors
logging.basicConfig(level=logging.ERROR, format="%(message)s",
                    datefmt="[%X]",
                    handlers=[RichHandler(rich_tracebacks=True)])
log = logging.getLogger("rich")


def load_yaml(yaml_config_file=""):
    """
    load config yaml files for onboardme and return as dicts
    """
    if path.exists(yaml_config_file):
        with open(yaml_config_file, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    else:
        # print(f"Config file we got was not present: {yaml_config_file}")
        return None


PWD = path.dirname(__file__)
DEFAULTS = load_yaml(f"{PWD}/config/onboardme_config.yml")
HOME_DIR = getenv("HOME")
SYSINFO = uname()
# this will be something like ('Darwin', 'x86_64')
OS = (SYSINFO.sysname, SYSINFO.machine)


def check_os_support():
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


def process_steps(steps=[], firewall=False, browser=False):
    """
    process which steps to run for which OS, which steps the user passed in,
    and then make sure dependent steps are always run.

    Returns a list of str type steps to run.

    # TODO: if 'capslock_to_control' in steps: map_caps_to_control()
    """
    if steps:
        steps_list = list(steps)
        # setting up vim is useless if we don't have a .vimrc
        if 'vim_setup' in steps_list and 'dot_files' not in steps_list:
            steps_list.append('dot_files')
        if browser:
            steps_list.append('browser_setup')
        if firewall and 'Linux' in OS:
            # currently don't have a great firewall on macOS, sans lulu
            steps_list.append('firewall_setup')

    removed_duplicates = set(steps_list)
    steps = list(removed_duplicates)
    default_order = DEFAULTS['steps'][OS[0]]

    # Rearrange list by other list order Using list comprehension
    result_steps = [ele for ele in default_order if ele in steps]

    return result_steps


def determine_logging_level(logging_string=""):
    """
    returns logging object for given logging string of one of the following:
    info, warn, error, debug
    """
    log_level = logging_string.upper()

    if log_level == "DEBUG":
        return logging.DEBUG
    elif log_level == "INFO":
        return logging.INFO
    elif log_level == "WARN":
        return logging.WARN
    elif log_level == "ERROR":
        return logging.ERROR
    else:
        raise Exception(f"Invalid log level: {logging_string}")


def fill_in_defaults(defaults={}, user_config={}, always_prefer_default=False):
    """
    Compares/Combines a default dict and another dict. Prefer default values
    only if the value is empty in the second dict. Then return new dict.
    """
    # log.debug("fill_in_defaults defaults:", defaults)
    # log.debug("fill_in_defaults user_config:", user_config)

    for key, value in user_config.items():
        # we have to iterate through the entire config file, and who knows how
        # many levels there are, so we use recursion of this function
        if type(value) is dict:
            result_config = fill_in_defaults(defaults[key], user_config[key],
                                             always_prefer_default)
            user_config[key] = result_config

        if not value or always_prefer_default:
            user_config[key] = defaults[key]

    return user_config


def process_configs(overwrite=False, repo="", git_branch="", pkg_mngrs=[],
                    pkg_groups=[], log_level="", log_file="", quiet=False,
                    firewall=False, remote_host="", steps=[]):
    """
    process the config in ~/.config/onboardme/config.yaml if it exists,
    then process the cli dict, and fill in defaults for anything not explicitly
    defined. Returns full final config as dict for use in script.
    """
    if remote_host:
        firewall = True
        if type(remote_host) is str:
            remote_host = [remote_host]

    cli_dict = {'package': {'managers': {OS[0]: pkg_mngrs},
                            'groups': pkg_groups},
                'log': {'file': log_file, 'level': log_level, 'quiet': quiet},
                'remote_hosts': remote_host,
                'firewall': firewall,
                'steps': {OS[0]: steps},
                'dot_files': {'overwrite': overwrite,
                              'git_url': repo, 'git_branch': git_branch}}

    # log.debug("cli_dict is: ", cli_dict)

    user_config_file = load_yaml(f'{HOME_DIR}/.config/onboardme/config.yaml')
    if user_config_file:
        # log.debug("🗂 ⚙️  user_config_file is", user_config_file)

        usr_cfgs = fill_in_defaults(DEFAULTS, user_config_file)
        # log.debug("after user_config_file filled in with defaults" + \
        #           " in process_user_config:", usr_cfgs)

        final_defaults = fill_in_defaults(cli_dict, usr_cfgs, True)
    else:
        final_defaults = fill_in_defaults(DEFAULTS, cli_dict)

    # log.debug(" final config after filling cli_dict in with defaults in "
    #           "process_user_config:", final_defaults)

    valid_steps = process_steps(final_defaults['steps'][OS[0]],
                                final_defaults['remote_hosts'])
    final_defaults['steps'][OS[0]] = valid_steps

    log_level = determine_logging_level(final_defaults['log']['level'])
    final_defaults['log']['level'] = log_level

    return final_defaults
