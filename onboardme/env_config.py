#!/usr/bin/env python3.10
# Onboarding script for macOS and Debian by jessebot@Linux.com
import logging
from os import getenv, path, uname
# rich helps pretty print everything
from rich.prompt import Confirm
from .console_logging import print_panel
import yaml


# user system env info
HOME_DIR = getenv("HOME")
SYSINFO = uname()
# this will be something like Darwin_x86_64
OS = f"{SYSINFO.sysname}_{SYSINFO.machine}"
with open(f"{path.dirname(__file__)}/config/config.yml", 'r') as yaml_file:
    OPTS = yaml.safe_load(yaml_file)


def parse_local_configs():
    """
    parse the local config yaml file if it exists
    """
    local_config_dir = f'{HOME_DIR}/.config/onboardme/config.yaml'
    if path.exists(local_config_dir):
        with open(local_config_dir, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
    return config


def check_os_support():
    """
    verify we're on a supported OS and ask to quit if not.
    """
    if SYSINFO.sysname != 'Linux' and SYSINFO.sysname != 'Darwin':
        msg = (f"[ohno]{SYSINFO.sysname}[/ohno] isn't officially supported. We"
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
        steps = set(steps)
        # setting up vim is useless if we don't have a .vimrc
        if 'vim_setup' in steps and 'dot_files' not in steps:
            steps.append('dot_files')
    else:
        steps = OPTS['steps'][SYSINFO.sysname]

        if 'Linux' in OS:
            # fonts are brew installed on macOS, docker grp only setup on linux
            steps.extend(['font_installation', 'groups_setup'])
            if firewall:
                # currently don't have a great firewall on macOS, sans lulu
                steps.append('firewall_setup')
            if browser:
                steps.append('browser_setup')
    return list(steps)


def determine_logging_level(logging_string=""):
    """
    returns logging object
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
    comparse a default dict and another dict and prefer default values
    if the value is empty in the the second dict, then return new dict
    """
    for key, value in user_config.items():
        if not value or always_prefer_default:
            user_config[key] = defaults[key]
        if type(value) is dict:
            for nested_key, nested_value in user_config[key].items():
                if not nested_value:
                    user_config[key][nested_key] = defaults[key][nested_key]
            if type(nested_value) is dict:
                for n2_key, n2_value in user_config[nested_key].items():
                    if not n2_value:
                        user_config[key][nested_key][n2_key] = \
                                defaults[key][nested_key][n2_key]

    current_steps = user_config['steps'][SYSINFO.sysname]
    steps = process_steps(current_steps, user_config['remote_hosts'])
    user_config['steps'][SYSINFO.sysname] = steps
    return user_config


def process_user_config(defaults={}, overwrite=False, repo="", git_branch="",
                        pkg_mngrs=[], pkg_groups=[], log_level="", log_file="",
                        quiet=False, firewall=False, remote_host="", steps=[]):
    """
    process the config in ~/.config/onboardme/config.yml if it exists
    and return variables as a dict for use in script, else return default opts
    """
    if not log_level:
        log_level = "warn"
    level = determine_logging_level(log_level)

    if remote_host:
        firewall = True
        if type(remote_host) is str:
            remote_host = [remote_host]

    cli_dict = {'package': {'managers': {SYSINFO.sysname: pkg_mngrs},
                            'groups': pkg_groups},
                'log': {'file': log_file, 'level': level, 'quiet': quiet},
                'remote_hosts': remote_host,
                'firewall': firewall,
                'steps': {SYSINFO.sysname: steps},
                'dot_files': {'overwrite': overwrite,
                              'git_url': repo, 'git_branch': git_branch}}

    # cli options are more important, but if none passed in, we check .config
    usr_cfg_file = path.join(HOME_DIR, '.config/onboardme/config.yml')

    if path.exists(usr_cfg_file):
        with open(usr_cfg_file, 'r') as yaml_file:
            user_config_file = yaml.safe_load(yaml_file)

        usr_cfgs = fill_in_defaults(cli_dict, user_config_file, True)
        return fill_in_defaults(defaults, usr_cfgs)
    else:
        return fill_in_defaults(defaults, cli_dict)
