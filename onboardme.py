#!/usr/bin/env python
# Generic onboarding script for mac osx
# jessebot@linux.com
import argparse
import json
import os
import subprocess
import shutil
import sys
import wget
from zipfile import ZipFile

# TODO: get better URLs like 'latest' or something for these hardcoded globals
ALFRED_URL = "https://cachefly.alfredapp.com/Alfred_4.0.8_1135.dmg"
BREW_URL = 'https://raw.githubusercontent.com/Homebrew/install/master/install'
SPECTACLE_URL = "https://s3.amazonaws.com/spectacle/downloads/Spectacle+1.2.zip"
# TODO: add option for custom install dir
HOME_DIR = os.getenv("HOME")


def download(url):
    """
    downloads a file from a given URL
    """
    try:
        dl_file = wget.download(url, HOME_DIR)
    except Exception as e:
        print("download bad: ", e)
    return dl_file


def is_installed(command_to_invoke):
    """
    just checks if a program already exists by trying to call it
    Takes command_to_invoke str var
    Returns true if command runs successfully
    """
    exit_code = os.system(command_to_invoke)
    if exit_code != 0:
        return False
    return True
    


def main():
    """
    Core function
    # TODO: add functioning arg parser

    # parse args
    parser = argparse.ArgumentParser(description='This is a generic onboarding script for mac osx')

    # parser.add_argument('--dryrun', action="store_true", default=False,
    #                    help="UNDER CONSTRUCTION. perform a Dry Run of the script," +
                             "which means, don't perform any writes to the system.")

    parser.add_argument('--file', default="obm_config.json", type=str,
                        help='Name of the JSON file for the config, defaults to: ' +
                             'obm_config')
    # TODO: add option for custom install dir

    res = parser.parse_args()
    # dry_run = res.dry_run
    config_file = res.file
    """
    #TODO: remove hardcoding
    config_file = "./obm_config.json"

    list_of_installs = process_json(config_file)

    for app in list_of_installs['install_apps']:
        if app == "alfred":
            if is_installed("ls /Applications/Alfred*"):
                print("\nAlfred is already installed :D")
            else:
                print("\nDownloading Alfred...")
                package = "open " + download(ALFRED_URL)
                print("\nInstalling Alfred...")
                subprocess = subproc(package, "Error with the alfred install")
        elif app == "brew":
            # TODO: process brew files
            if is_installed("brew help"):
                print("\nBrew is already installed :D")
            else:
                print("\nInstalling Brew...")
                cmd = '/usr/bin/ruby -e "$(curl -fsSL {0})"'.format(BREW_URL)
                os.system(cmd)
        elif app == "iterm2":
            # TODO: Personal settings
            print("\nBrew installing iterm2...")
            cmd = "brew cask install iterm2"
            subprocess = subproc(cmd, "\nerror with the iterm2 install")
        elif app == "spectacle":
            print("\nBrew installing spectacle...")
            cmd = "brew cask install spectacle"
            subprocess = subproc(cmd, "\nerror with the spectacle install")
        elif app == "rc_files":
            print("\nDownloading rc files via git...")
            # I know, I know, but like... git isn't installed everywhere, fam
            git_URL = list_of_installs["rc_URL"]
            cmd = "svn checkout " + git_URL
            subprocess = subproc(cmd, "\nerror with the rc files download...")
            dot_files_dir = git_URL.split('/')[-1]
            for root, dirs, files in os.walk(dot_files_dir, topdown=False):
                for name in files:
                    os.rename(os.path.join(root, name),
                            os.path.join(HOME_DIR, name))
                for name in dirs:
                    # hacky
                    if name != ".svn":
                        os.rename(os.path.join(root, name),
                                os.path.join(HOME_DIR, name))
            shutil.rmtree("./" + dot_files_dir)
        elif app == "wallpapers":
            print("Downloading wallpapers...")
            # create a special directory for this
            pic_dir = HOME_DIR + "/Pictures/wallpapers"
            os.mkdir(pic_dir) 
            URL = list_of_installs["URL"]
            package = download(URL, pic_dir)
            package_name = package.split('/')[::-1]
            destination = "." + "/".join([HOME_DIR, "Pictures/wallpapers",
                                          package_name])
            os.rename(package, destination)


def process_json(config_file):
    """
    process the core json config file
    """
    with open(config_file, 'r') as json_f:
        json_data = json.load(json_f)

    print(json_data)
    return json_data


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
