#!/usr/bin/env python3.11
"""
       Name:
DESCRIPTION:
     AUTHOR:
    LICENSE: GNU AFFERO GENERAL PUBLIC LICENSE Version 3
"""
from importlib.metadata import version as get_version
from xdg_base_dirs import xdg_config_home
from os import getenv, path, uname


# version of onboardme
VERSION = get_version('onboardme')

# pathing
XDG_CONFIG_DIR = xdg_config_home()
ONBOARDME_CONFIG_DIR = path.join(xdg_config_home(), 'onboardme')
PWD = path.dirname(__file__)
HOME_DIR = getenv("HOME")

# env
SYSINFO = uname()
# this will be something like ('Darwin', 'x86_64')
OS = (SYSINFO.sysname, SYSINFO.machine)

# step config is different per OS
STEPS = ['dot_files','packages','font_setup','neovim_setup','group_setup']
if OS[0] == 'Darwin':
    STEPS.append('sudo_setup')

# package manager config is different per OS
PKG_MNGRS = ['brew','pip3.11']
if OS[0] == 'Linux':
    PKG_MNGRS.extend(['apt','snap','flatpak'])
