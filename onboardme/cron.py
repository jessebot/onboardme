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
    user_crontab = f'{HOME_DIR}/.config/cron/user/crontab'

    print_header('⏰ [i]crontab[/i] installations')
    if 'Linux' in OS:
        root_crontab = f'{HOME_DIR}/.config/cron/root/crontab'
        # install root level cronjobs
        if path.exists(root_crontab):
            log.info('Installing root crontab.')
            subproc([f'sudo crontab {root_crontab}'])
            print_msg('\n[i]root crontab installed.')

    # install user level cronjobs
    if path.exists(user_crontab):
        log.info('Installing user crontab.')
        username = getuser()
        subproc([f'crontab {HOME_DIR}/.config/cron/user/crontab'])
        print_msg('\n[i]User crontab installed.')
