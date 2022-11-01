#!/usr/bin/env python3.10
"""
    NAME:           Onboardme
    DESCRIPTION:    Program to take care of a bunch of onboarding tasks for new
                    machines running macOS and/or Debian.
    AUTHOR:         Jesse Hitch
    LICENSE:        GNU AFFERO GENERAL PUBLIC LICENSE
"""
from click import option, command, Choice
import dbm
import importlib
import logging
import sys

# rich helps pretty print everything
from rich.console import Console
from rich.table import Table
from rich.logging import RichHandler

# custom libs
from .help_text import RichCommand, options_help
from .env_config import check_os_support, process_configs, OS
from .env_config import DEFAULTS as OPTS
from .console_logging import print_panel


HELP = options_help()


def setup_logger(log_level, log_file=""):
    """
    Sets up rich logger and stores the values for it in a db for future import
    in other files. Returns logging.getLogger("rich")
    """
    # set the logger opts for all files
    with dbm.open('log_cache', 'c') as db:
        db['level'] = str(log_level)
        db['file'] = log_file

    log_opts = {'level': log_level,
                'format': "%(message)s",
                'datefmt': "[%X]",
                'handlers': [RichHandler(rich_tracebacks=True)]}

    # we only log to a file if one was passed into config.yaml or the cli
    if log_file:
        log_opts['console'] = Console(file=log_file)

    # this uses the log_opts dictionary as parameters to logging.basicConfig()
    logging.basicConfig(**log_opts)
    return logging.getLogger("rich")


def print_manual_steps():
    """
    Just prints out the final steps to be done manually, til we automate them
    """
    # table to print the results of all the files
    table = Table(expand=True, box=None,
                  title=" ",
                  row_styles=["", "dim"],
                  border_style="dim",
                  header_style="cornflower_blue",
                  title_style="light_steel_blue")
    table.add_column("Don't forget these (currently) manual tasks",
                     justify="center")

    table.add_row(" ")
    table.add_row("Import RSS feeds config into FluentReader")
    table.add_row("Import subscriptions into FreeTube")
    table.add_row("⌨️  Set CAPSLOCK to control")
    table.add_row("Install cronjobs you need from ~/.cron")
    table.add_row("Load your BASH config: [green]source .bashrc[/]")
    table.add_row("Reboot, as [turquoise2]docker[/] demands it")
    table.add_row(" ")
    table.add_row("If you need any help, check the docs:")
    table.add_row("[cyan][link=https://jessebot.github.io/onboardme]"
                  "jessebot.github.io/onboardme[/link]")
    table.add_row(" ")

    print_panel(table, '[green]♥ ˖⁺‧Success‧⁺˖ ♥')
    return True


# Click is so ugly, and I'm sorry we're using it for cli parameters here, but
# this allows us to use rich.click for pretty prettying the help interface
# each of these is an option in the cli and variable we use later on
@command(cls=RichCommand)
@option('--log_level', '-l', metavar='LOGLEVEL', help=HELP['log_level'],
        type=Choice(['debug', 'info', 'warn', 'error']))
@option('--log_file', '-o', metavar='LOGFILE', help=HELP['log_file'])
@option('--quiet', '-q', is_flag=True, help=HELP['quiet'])
@option('--steps', '-s', metavar='STEP', multiple=True,
        type=Choice(OPTS['steps'][OS[0]]), help=HELP['steps'])
@option('--git_url', '-u', metavar='URL', help=HELP['git_url'])
@option('--git_branch', '-b', metavar='BRANCH', help=HELP['git_branch'])
@option('--overwrite', '-O', is_flag=True, help=HELP['overwrite'])
@option('--pkg_managers', '-p', metavar='PKG_MANAGER', multiple=True,
        type=Choice(OPTS['package']['managers'][OS[0]]),
        help=HELP['pkg_managers'])
@option('--pkg_groups', '-g', metavar='PKG_GROUP', multiple=True,
        type=Choice(['default', 'gaming', 'media', 'devops']),
        help=HELP['pkg_groups'])
@option('--firewall', '-f', is_flag=True, help=HELP['firewall'])
@option('--remote_host', '-r', metavar="IP_ADDR", multiple=True,
        help=HELP['remote_host'])
def main(log_level: str = "",
         log_file: str = "",
         quiet: bool = False,
         steps: str = "",
         git_url: str = "",
         git_branch: str = "",
         overwrite: bool = False,
         pkg_managers: str = "",
         pkg_groups: str = "",
         firewall: bool = False,
         remote_host: str = ""):
    """
    Uses config in the script repo in config/packages.yml and config/config.yml
    If run with no options on Linux, it will install brew, pip3.10, apt,
    flatpak, and snap packages. On mac, it only installs brew/pip3.10 packages.
    config loading tries to load: cli options and then .config/onboardme/*
    """
    # before we do anything, we need to make sure this OS is supported
    check_os_support()

    # then process any local user config files, cli opts, and defaults
    user_prefs = process_configs(overwrite, git_url, git_branch, pkg_managers,
                                 pkg_groups, log_level, log_file, quiet,
                                 firewall, remote_host, steps)

    log = setup_logger(user_prefs['log']['level'], user_prefs['log']['file'])

    log.debug("User passed in the following preferences:", user_prefs)

    # actual heavy lifting of onboardme happens in these
    for step in user_prefs['steps'][OS[0]]:

        if step == 'dot_files':
            from .dot_files import setup_dot_files
            # this creates a live git repo out of your home directory
            df_prefs = user_prefs['dot_files']
            setup_dot_files(OS, df_prefs['overwrite'],
                            df_prefs['git_url'], df_prefs['git_branch'])

        elif step == 'packages':
            from .pkg_management import run_pkg_mngrs
            pkg_mngrs = user_prefs['package']['managers'][OS[0]]
            pkg_groups = user_prefs['package']['groups']
            log.debug(pkg_mngrs, pkg_groups)
            run_pkg_mngrs(pkg_mngrs, pkg_groups)

        elif step in ['vim_setup', 'neovim_setup', 'font_setup']:
            # import step from ide_setup.py in same directory
            importlib.import_module(f'onboardme.ide_setup', package=f'.{step}')
            func = getattr(ide_setup, step)
            func()

    if 'firewall_setup' in steps:
        from .firewall import configure_firewall
        configure_firewall(remote_host)

    print_manual_steps()
    return


if __name__ == '__main__':
    main()
