#!/usr/bin/env python3.10
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
    # TODO: is there a python cron library 🤔 install .cron dir? (is there a
    # standard in where cronjobs live for users [preferably in the home dir?)
    # that works on both macos and debian?
