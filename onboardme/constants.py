#!/usr/bin/env python3.11
"""
       Name: onboardme constants
DESCRIPTION: constants for onboardme
     AUTHOR: @jessebot
    LICENSE: GNU AFFERO GENERAL PUBLIC LICENSE Version 3
"""
from importlib.metadata import version as get_version
from xdg_base_dirs import xdg_config_home
from os import getenv, path, uname
from pathlib import Path
from shutil import copy
import wget
from ruamel.yaml import YAML


# version of onboardme
VERSION = get_version('onboardme')

# pathing
XDG_CONFIG_DIR =  path.join(xdg_config_home(), "onboardme")
XDG_CONFIG_FILE = path.join(XDG_CONFIG_DIR, "/config.yml")
PWD = path.dirname(__file__)
HOME_DIR = getenv("HOME")

# env
SYSINFO = uname()
# this will be something like this for old macs: ('Darwin', 'x86_64')
# this will be something like this for M1 and latest macs: ('Darwin', 'arm64')
OS = (SYSINFO.sysname, SYSINFO.machine)

# step config is different per OS
STEPS = ['dot_files','packages','font_setup','neovim_setup','group_setup']
if OS[0] == 'Darwin':
    STEPS.append('sudo_setup')

# package manager config is different per OS
PKG_MNGRS = ['brew','pip3.11']
if OS[0] == 'Linux':
    PKG_MNGRS.extend(['apt','snap','flatpak'])

# grabs the default packaged config file from default dot files
DEFAULT_CONFIG_FILE = path.join(PWD, 'config/default_config.yml')

default_dotfiles = ("https://raw.githubusercontent.com/jessebot/dot_files/"
                    "main/.config/onboardme/")

if OS[0] == 'Linux' and OS[1] == 'aarch64':
    default_dotfiles = ("https://raw.githubusercontent.com/jessebot/dot_files/"
                        "docker-arm64-only/.config/onboardme/")

def load_cfg(config_file: str = 'config.yml') -> dict:
    """
    load yaml config files for onboardme
    """
    config_full_path = path.join(XDG_CONFIG_DIR, config_file)
    print(config_full_path)

    # create default pathing and config file if it doesn't exist
    if not path.exists(config_full_path):
        if config_file == "config.yml": 
            copy(DEFAULT_CONFIG_FILE, config_full_path)
        else:
            Path(XDG_CONFIG_DIR).mkdir(parents=True, exist_ok=True)
            # downloads a default config file from default dot files
            wget.download(default_dotfiles + config_file, config_full_path)

    yaml = YAML()

    with open(config_full_path, 'r') as yaml_file:
        return yaml.load(yaml_file)


INITIAL_USR_CONFIG = load_cfg()

DEFAULT_PKG_GROUPS = INITIAL_USR_CONFIG['package']['groups']['default']
OPT_PKG_GROUPS = INITIAL_USR_CONFIG['package']['groups']['optional']
