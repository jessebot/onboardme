"""
       Name:
DESCRIPTION:
     AUTHOR:
    LICENSE: GNU AFFERO GENERAL PUBLIC LICENSE Version 3
"""
from importlib.metadata import version as get_version
from xdg_base_dirs import xdg_config_home
from os import getenv, path, uname
from pathlib import Path
import wget
import yaml


# version of onboardme
VERSION = get_version('onboardme')

# pathing
XDG_CONFIG_DIR = xdg_config_home()
PWD = path.dirname(__file__)
HOME_DIR = getenv("HOME")

# env
SYSINFO = uname()
# this will be something like this for old macs: ('Darwin', 'x86_64')
# this will be something like this for M1 and latest macs: ('Darwin', 'arm64')
OS = (SYSINFO.sysname, SYSINFO.machine)

# step config is different per OS
STEPS = ['dot_files','packages','cron','font_setup','neovim_setup','group_setup']
if OS[0] == 'Darwin':
    STEPS.append('sudo_setup')

# package manager config is different per OS
PKG_MNGRS = ['brew','pip3.12','pip3.11','pipx']
if OS[0] == 'Linux':
    PKG_MNGRS.extend(['apt','snap','flatpak'])


default_dotfiles = ("https://raw.githubusercontent.com/jessebot/dot_files/"
                    "main/.config/onboardme/")

if OS[0] == 'Linux' and OS[1] == 'aarch64':
    default_dotfiles = ("https://raw.githubusercontent.com/jessebot/dot_files/"
                        "docker-arm64-only/.config/onboardme/")

def load_cfg(config_file='config.yml') -> dict:
    """
    load yaml config files for onboardme
    """
    config_dir = path.join(xdg_config_home(), 'onboardme')
    config_full_path = path.join(config_dir, config_file)

    # create default pathing and config file if it doesn't exist
    if not path.exists(config_full_path):
        Path(config_dir).mkdir(parents=True, exist_ok=True)
        # downloads a default config file from default dot files
        wget.download(default_dotfiles + config_file, config_full_path)

    with open(config_full_path, 'r') as yaml_file:
        return yaml.safe_load(yaml_file)


USR_CONFIG_FILE = load_cfg()

DEFAULT_PKG_GROUPS = USR_CONFIG_FILE['package']['groups']['default']
OPT_PKG_GROUPS = USR_CONFIG_FILE['package']['groups']['optional']
