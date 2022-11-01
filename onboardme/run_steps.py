#!/usr/bin/env python3.10
"""
    Name:
    DESCRIPTION:
    AUTHOR:         https://github.com
    LICENSE:        GNU AFFERO GENERAL PUBLIC LICENSE Version 3
"""
from .dot_files import setup_dot_files
from .pkg_management import run_pkg_mngrs
from .ide_setup import vim_setup, neovim_setup, install_fonts
from .firewall import setup_nix_groups, configure_firewall
