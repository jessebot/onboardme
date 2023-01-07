#!/usr/bin/env python3.11
"""
       Name:
DESCRIPTION:
     AUTHOR:
    LICENSE: GNU AFFERO GENERAL PUBLIC LICENSE Version 3
"""
from importlib.metadata import version as get_version
from xdg import xdg_config_home
from os import getenv, path, uname


# version of onboardme
VERSION = get_version('onboardme')

# pathing
XDG_CONFIG_DIR = path.join(xdg_config_home(), 'onboardme')
PWD = path.dirname(__file__)
HOME_DIR = getenv("HOME")

# env
SYSINFO = uname()
# this will be something like ('Darwin', 'x86_64')
OS = (SYSINFO.sysname, SYSINFO.machine)
