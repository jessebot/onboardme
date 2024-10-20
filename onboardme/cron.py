"""
NAME:    onboardme.cron
DESC:    install cron jobs for the user and root
AUTHORS:  Jesse Hitch
LICENSE: GNU AFFERO GENERAL PUBLIC LICENSE
"""

import logging as log
from os import path
from pathlib import Path

# custom libs
from getpass import getuser

from .constants import HOME_DIR, OS
from .console_logging import print_header, print_msg
from .subproc import subproc


def cron_setup() -> None:
    """
    Installs crontab to run onboardme for user only functions

    On Linux:
        installs crontab for root to run apt commands
    """
    print_header('⏰ [i]crontab[/i] installations')
    if 'Linux' in OS:
        cron_dir = "/etc/crontab.d"

        # install root level cronjobs
        root_crontab = f'{HOME_DIR}/.config/cron/root/crontab'

        # do a shallow clone of the repo
        if path.exists(root_crontab):
            log.info('Installing root crontab.')
            subproc([f'sudo cp {root_crontab} {cron_dir}/root'])
            print_msg('[i]root crontab installed.')
    else:
        cron_dir = "/var/at/tabs"

    # install user level cronjobs
    user_crontab = f'{HOME_DIR}/.config/cron/user/crontab'
    if path.exists(user_crontab):
        log.info('Installing user crontab.')
        username = getuser()
        subproc([f'sudo cp {user_crontab} {cron_dir}/{username}'])
        print_msg('[i]User crontab installed.')
