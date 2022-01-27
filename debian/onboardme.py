#!/usr/bin/env python3
# Generic onboarding script for mac osx
# jessebot@linux.com
import argparse
import json
import os
import subprocess
import sys

HOME_DIR = os.getenv("HOME")


def main():
    """
    Core function
    """
    help = 'This is a generic onboarding script for mint'
    parser = argparse.ArgumentParser(description=help)
    dr_help = "perform a Dry Run of the script"
    parser.add_argument('--dryrun', action="store_true", default=False,
                       help=dr_help)
    res = parser.parse_args()
    dry_run = res.dry_run

    base_apt_install = "apt-get install"
    apt_install = base_apt_install + " <apt_packages.txt"
    if not dry_run:
        apt_install = base_apt_install + " -y <apt_packages.txt"

    subprocess = subproc(apt_install, "Error with package installs :shrug:")


def subproc(cmd, help="Something went wrong!"):
    """
    Takes a commmand to run in BASH, as well as optional
    help text, both str
    """
    command = cmd.split()
    res_err = ""
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        return_code = p.returncode
        res_out = p.communicate()
        # check return code, raise error if failure
        if return_code != 0:
            err = "Return code was not zero! It was:" + \
                  " {0} see res: ".format(return_code)
            raise Exception(err)
    except Exception as e:
        if res_err:
            print("ERROR: " + " ".join([help, e, res_out]))

    return res_out


if __name__ == '__main__':
    main()
