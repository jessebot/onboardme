#!/usr/bin/env python3.10
"""
       Name: onbaordme.sudo_setup
DESCRIPTION: setup pam module for sudo and add user to sudo group
     AUTHOR: Jesse Hitch
    LICENSE: GNU AFFERO GENERAL PUBLIC LICENSE Version 3
"""

import logging as log
from os import geteuid
from os import system as check_response

# custom libs
from .console_logging import print_header, print_sub_header
from .subproc import subproc


def setup_sudo():
    """
    make sure we're root on mac and kick off setting up sudo with touchid
    Returns True
    """
    print_header("🔒 Setting up sudo")

    # check if running as root
    if geteuid() != 0:
        subproc(["sudo onboardme -s sudo_setup"], spinner=False)
        print_sub_header("🧑‍💻 sudo using TouchId is enabled.")
    else:
        enable_sudo_with_touchid()
    return True


def enable_sudo_with_touchid():
    """
    We look for this line in /etc/pam.d/sudo:
        auth       sufficient     pam_tid.so
    If not found, we add it.
    return True
    """
    pam_file = "/etc/pam.d/sudo"
    if check_response(f'grep "pam_tid.so" {pam_file}') != 0:
        log.info(f"TouchID not found in {pam_file}. Attempting to add it.")

        # read in the file and modify the second line to have pam_tid.so
        new_contents = []
        with open(pam_file, 'r') as file_contents:
            for index, line in enumerate(file_contents.readlines()):
                new_contents.append(line)
                if index == 1:
                    touchid = "auth       sufficient     pam_tid.so\n"
                    new_contents.append(touchid)

        # write back the altered file
        with open(pam_file, 'w') as new_file_contents:
            for line in new_contents:
                new_file_contents.write(line)
    return True
