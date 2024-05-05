"""
       Name: onbaordme.sudo_setup
DESCRIPTION: setup pam module for sudo and add user to sudo group
     AUTHOR: Jesse Hitch
    LICENSE: GNU AFFERO GENERAL PUBLIC LICENSE Version 3
"""
from os import geteuid
from os.path import exists
from os import system as check_response

# custom libs
from .console_logging import print_header, print_sub_header
from .subproc import subproc


def setup_sudo() -> None:
    """
    make sure we're root on mac and kick off setting up sudo with touchid
    """
    print_header("🔒 Setting up sudo")

    # check if running as root
    if geteuid() != 0:
        subproc(["sudo onboardme -s sudo_setup"], spinner=False)
        print_sub_header("🧑‍💻 sudo using TouchId is enabled.")
    else:
        enable_sudo_with_touchid()


def enable_sudo_with_touchid() -> None:
    """
    We look for this line in /etc/pam.d/sudo_local:
    auth       sufficient     pam_tid.so

    If file doesn't exiswt or line not found, we add it.
    """
    def write_touch_id_sudo(pam_file):
        # write back the altered file
        with open(pam_file, 'w') as new_file_contents:
            new_file_contents.write("auth       sufficient     pam_tid.so\n")

    pam_file = "/etc/pam.d/sudo_local"
    touch_id_line = "^auth       sufficient     pam_tid.so"
    if exists(pam_file):
        if check_response(f'grep "{touch_id_line}" {pam_file}') != 0:
            write_touch_id_sudo(pam_file)
    else:
        write_touch_id_sudo(pam_file)
