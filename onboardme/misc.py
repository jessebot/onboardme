"""
    Name:           onboardme.misc
    DESCRIPTION:    this is where I'm putting extra functions
    AUTHOR:         https://github.com/jessebot
    LICENSE:        GNU AFFERO GENERAL PUBLIC LICENSE Version 3
"""
from .subproc import subproc
from .console_logging import print_header


def map_caps_to_control():
    """
    NOT IN USE. NEEDS TLC.
    Maps capslock to control. This is ugly and awful and untested
    """
    print_header("⌨️  Mapping capslock to control...")
    subproc(["setxkbmap -layout us -option ctrl:nocaps"])


def setup_cronjobs():
    """
    setup any important cronjobs/alarms.
    Currently just adds nightly updates and reminders to take breaks
    """
    print_header("⏰ Installing new cronjobs...")
    print("\n")
