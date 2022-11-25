"""
    NAME:           onboardme
    DESCRIPTION:    Program to take care of a bunch of onboarding tasks for new
                    machines running macOS and/or Debian, including:
                      dot_files, managing packages, ide_setup, group management
    AUTHOR:         Jesse Hitch
    LICENSE:        GNU AFFERO GENERAL PUBLIC LICENSE
"""

from click import option, command, Choice
from importlib import import_module
from importlib.metadata import version as get_version
import logging
from rich.console import Console
from rich.logging import RichHandler
from .help_text import RichCommand, options_help
from .env_config import check_os_support, OS, process_configs, USR_CONFIG_FILE
from .env_config import DEFAULTS as OPTS
from .console_logging import print_manual_steps
from .dot_files import setup_dot_files
from .pkg_management import run_pkg_mngrs
from .sudo_setup import setup_sudo
from .firewall import configure_firewall


HELP = options_help()


def setup_logger(level="", log_file=""):
    """
    Sets up rich logger and stores the values for it in a db for future import
    in other files. Returns logging.getLogger("rich")
    """
    # determine logging level
    if not level:
        if USR_CONFIG_FILE and 'log' in USR_CONFIG_FILE:
            level = USR_CONFIG_FILE['log']['level']
        else:
            level = 'warn'

    log_level = getattr(logging, level.upper(), None)

    # these are params to be passed into logging.basicConfig
    opts = {'level': log_level, 'format': "%(message)s", 'datefmt': "[%X]"}

    # we only log to a file if one was passed into config.yaml or the cli
    if not log_file:
        if USR_CONFIG_FILE:
            log_file = USR_CONFIG_FILE['log'].get('file', None)

    # rich typically handles much of this but we don't use rich with files
    if log_file:
        opts['filename'] = log_file
        opts['format'] = "%(asctime)s %(levelname)s %(funcName)s: %(message)s"
    else:
        rich_handler_opts = {'rich_tracebacks': True}
        # 10 is the DEBUG logging level int value
        if log_level == 10:
            # log the name of the function if we're in debug mode :)
            opts['format'] = "[bold]%(funcName)s()[/bold]: %(message)s"
            rich_handler_opts['markup'] = True

        opts['handlers'] = [RichHandler(**rich_handler_opts)]

    # this uses the opts dictionary as parameters to logging.basicConfig()
    logging.basicConfig(**opts)

    if log_file:
        return None
    else:
        return logging.getLogger("rich")


# @option('--quiet', '-q', is_flag=True, help=HELP['quiet'])
# Click is so ugly, and I'm sorry we're using it for cli parameters here, but
# this allows us to use rich.click for pretty prettying the help interface
# each of these is an option in the cli and variable we use later on
@command(cls=RichCommand)
@option('--log_level', '-l', metavar='LOGLEVEL', help=HELP['log_level'],
        type=Choice(['debug', 'info', 'warn', 'error']))
@option('--log_file', '-o', metavar='LOGFILE', help=HELP['log_file'])
@option('--steps', '-s', metavar='STEP', multiple=True,
        type=Choice(OPTS['steps'][OS[0]]), help=HELP['steps'])
@option('--git_url', '-u', metavar='URL', help=HELP['git_url'])
@option('--git_branch', '-b', metavar='BRANCH', help=HELP['git_branch'])
@option('--overwrite', '-O', is_flag=True, help=HELP['overwrite'])
@option('--pkg_managers', '-p', metavar='PKG_MANAGER', multiple=True,
        type=Choice(OPTS['package']['managers'][OS[0]]),
        help=HELP['pkg_managers'])
@option('--pkg_groups', '-g', metavar='PKG_GROUP', multiple=True,
        type=Choice(['default', 'gaming', 'gui', 'devops']),
        help=HELP['pkg_groups'])
@option('--firewall', '-f', is_flag=True, help=HELP['firewall'])
@option('--remote_host', '-r', metavar="IP_ADDR", multiple=True,
        help=HELP['remote_host'])
@option('--version', is_flag=True, help=HELP['version'])
def main(log_level: str = "",
         log_file: str = "",
         steps: str = "",
         git_url: str = "",
         git_branch: str = "",
         overwrite: bool = False,
         pkg_managers: str = "",
         pkg_groups: str = "",
         firewall: bool = False,
         remote_host: str = "",
         version: bool = False):
    """
    Uses config in the script repo in config/packages.yml and config/config.yml
    If run with no options on Linux, it will install brew, pip3.11, apt,
    flatpak, and snap packages. On mac, it only installs brew/pip3.11 packages.
    config loading tries to load: cli options and then .config/onboardme/*
    """

    # only return the version if --version was passed in
    if version:
        print(f'\n🎉 v{get_version("onboardme")}\n')
        return True

    # before we do anything, we need to make sure this OS is supported
    check_os_support()

    # setup logging immediately
    log = setup_logger(log_level, log_file)

    # then process any local user config files, cli opts, and defaults
    usr_pref = process_configs(overwrite, git_url, git_branch, pkg_managers,
                               pkg_groups, firewall, remote_host, steps)

    if log:
        log.debug(f"User passed in the following preferences:\n{usr_pref}\n")
    else:
        logging.debug(f"User passed in the following preferences:\n{usr_pref}")

    # actual heavy lifting of onboardme happens in these
    for step in usr_pref['steps'][OS[0]]:

        if step == 'dot_files':
            # this creates a live git repo out of your home directory
            df_prefs = usr_pref['dot_files']
            setup_dot_files(OS, df_prefs['overwrite'],
                            df_prefs['git_url'], df_prefs['git_branch'])

        elif step == 'packages':
            pkg_mngrs = usr_pref['package']['managers'][OS[0]]
            pkg_groups = usr_pref['package']['groups']
            run_pkg_mngrs(pkg_mngrs, pkg_groups)

        elif step in ['vim_setup', 'neovim_setup', 'font_setup']:
            # import step's function from ide_setup.py in same directory
            import_module('onboardme.ide_setup', package=f'.{step}')
            func = getattr(ide_setup, step)
            func()

        elif step == 'sudo_setup':
            # if we're not running as root, kick off another process
            setup_sudo()

    if 'firewall_setup' in steps:
        configure_firewall(remote_host)

    print_manual_steps()
    return


if __name__ == '__main__':
    main()
