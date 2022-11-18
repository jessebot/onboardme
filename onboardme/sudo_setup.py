#!/usr/bin/env python3.10
"""
       Name: onbaordme.sudo_setup
DESCRIPTION: setup pam module for sudo and add user to sudo group
     AUTHOR: Jesse Hitch
    LICENSE: GNU AFFERO GENERAL PUBLIC LICENSE Version 3
"""

import logging as log
from os import geteuid

from .subproc import subproc


# custom libs
# from .env_config import OS


def setup_sudo():
    """
    make sure we're root and kick off setting up sudo with touchid
    """
    # check if running as root
    if geteuid() != 0:
        subproc(["sudo onboardme -s sudo_setup"], spinner=False)
    else:
        enable_sudo_with_touchid()


def enable_sudo_with_touchid():
    """
    We look for this line in /etc/pam.d/sudo:
        auth       sufficient     pam_tid.so
    If not found, we add it.
    return True
    """
    pam_file = "/etc/pam.d/sudo"
    if type(subproc([f'grep "pam_tid.so" {pam_file}'])) is not str:
        log.info(f"TouchID not found in {pam_file}. Attempting to add it.")

        # read in the file and modify the second line to have pam_tid.so
        new_contents = []
        with open(pam_file, 'r') as file_contents:
            for index, line in enumerate(file_contents.readlines()):
                new_contents.append(line)
                if index == 1:
                    new_contents.append("auth       sufficient     pam_tid.so\n")

        # write back the altered file
        with open(pam_file, 'w') as new_file_contents:
            for line in new_contents:
                new_file_contents.write(line)

    return True
