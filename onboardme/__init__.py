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
import logging
from rich.logging import RichHandler
from .help_text import RichCommand, options_help
from .constants import (DEFAULT_PKG_GROUPS,
                        OPT_PKG_GROUPS,
                        OS,
                        PKG_MNGRS,
                        STEPS,
                        VERSION,
                        INITIAL_USR_CONFIG,
                        load_cfg)
from .env_config import check_os_support, process_configs
from .console_logging import print_manual_steps
from .dot_files import setup_dot_files
from .packages.pkg_management import run_pkg_mngrs
from .sudo_setup import setup_sudo
from .firewall import configure_firewall
from .tui import launch_config_tui


HELP = options_help()
LOG_LEVEL = 'warn'
LOG_DICT = INITIAL_USR_CONFIG.get('log', None)
if LOG_DICT:
    LOG_LEVEL = LOG_DICT.get('level', 'warn')
try:
    LOG_FILE = INITIAL_USR_CONFIG['log']['file']
except KeyError:
    LOG_FILE = None


def setup_logger(level="", log_file=""):
    """
    Sets up rich logger and stores the values for it in a db for future import
    in other files. Returns logging.getLogger("rich")
    """
    # determine logging level
    if not level:
        level = LOG_LEVEL

    log_level = getattr(logging, level.upper(), None)

    # these are params to be passed into logging.basicConfig
    opts = {'level': log_level, 'format': "%(message)s", 'datefmt': "[%X]"}

    # we only log to a file if one was passed into config.yml or the cli
    if not log_file:
        log_file = LOG_FILE

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


# Click is so ugly, and I'm sorry we're using it for cli parameters here, but
# this allows us to use rich.click for pretty prettying the help interface
# each of these is an option in the cli and variable we use later on
@command(cls=RichCommand)
@option('--log_level',
        '-l',
        metavar='LOGLEVEL',
        help=HELP['log_level'],
        type=Choice(['debug', 'info', 'warn', 'error']),
        default=LOG_LEVEL)
@option('--log_file',
        '-o',
        metavar='LOGFILE',
        help=HELP['log_file'],
        default=LOG_FILE)
@option('--interactive',
        '-i',
        help=HELP['interactive'],
        is_flag=True,
        default=False)
@option('--steps',
        '-s',
        metavar='STEP',
        multiple=True,
        type=Choice(STEPS),
        help=HELP['steps'],
        default=INITIAL_USR_CONFIG['steps'][OS[0]])
@option('--git_url',
        '-u',
        metavar='URL',
        help=HELP['git_url'],
        default=INITIAL_USR_CONFIG['dot_files']['git_url'])
@option('--git_branch',
        '-b',
        metavar='BRANCH',
        help=HELP['git_branch'],
        default=INITIAL_USR_CONFIG['dot_files']['git_branch'])
@option('--git_config_dir',
        '-d',
        metavar='PATH',
        help=HELP['git_config_dir'],
        default=INITIAL_USR_CONFIG['dot_files']['git_config_dir'])
@option('--overwrite',
        '-O',
        is_flag=True,
        help=HELP['overwrite'],
        default=INITIAL_USR_CONFIG['dot_files']['overwrite'])
@option('--pkg_managers',
        '-p',
        metavar='PKG_MANAGER',
        multiple=True,
        type=Choice(PKG_MNGRS),
        help=HELP['pkg_managers'],
        default=INITIAL_USR_CONFIG['package']['managers'][OS[0]])
@option('--pkg_groups',
        '-g',
        metavar='PKG_GROUP',
        multiple=True,
        type=Choice(DEFAULT_PKG_GROUPS + OPT_PKG_GROUPS),
        help=HELP['pkg_groups'],
        default=DEFAULT_PKG_GROUPS)
@option('--firewall',
        '-f',
        is_flag=True,
        help=HELP['firewall'],
        default=INITIAL_USR_CONFIG['firewall'].get('enabled', False))
@option('--remote_host',
        '-r',
        metavar="IP_ADDR",
        multiple=True,
        help=HELP['remote_host'],
        default=INITIAL_USR_CONFIG.get('remote_hosts', None))
@option('--no_upgrade',
        '-n',
        help=HELP['no_upgrade'],
        default=False,
        is_flag=True)
@option('--version',
        is_flag=True,
        help=HELP['version'],
        default=False)
def main(log_level: str,
         log_file: str,
         interactive: bool,
         steps: str,
         git_url: str,
         git_branch: str,
         git_config_dir: str,
         overwrite: bool,
         pkg_managers,
         pkg_groups,
         firewall,
         remote_host,
         no_upgrade,
         version) -> bool:
    """
    If run with no options on Linux, it will install brew, pip3.11, apt,
    flatpak, and snap packages. On mac, it only installs brew/pip3.11 packages.
    config loading tries to load: cli options and then defaults back to:
    $XDG_CONFIG_HOME/onboardme/config.yml
    """

    # only return the version if --version was passed in
    if version:
        print(f'\n🎉 v{VERSION}\n')
        return True

    # before we do anything, we need to make sure this OS is supported
    check_os_support()

    # setup logging immediately
    log = setup_logger(log_level, log_file)

    # makes sure we only overwrite config file prefs if cli opts are passed in
    usr_pref = process_configs(overwrite,
                               git_url,
                               git_branch,
                               git_config_dir,
                               pkg_managers,
                               pkg_groups, 
                               firewall,
                               remote_host,
                               steps,
                               log_file,
                               log_level)

    pkg_mngrs_list_of_dicts = load_cfg('packages.yml')

    if interactive or usr_pref['tui']['enabled']:
        launch_config_tui(usr_pref, pkg_mngrs_list_of_dicts)

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
                            df_prefs['git_url'], df_prefs['git_branch'],
                            df_prefs['git_config_dir'])

        elif step == 'packages':
            pkg_mngrs = usr_pref['package']['managers'][OS[0]]
            pkg_groups = usr_pref['package']['groups']
            run_pkg_mngrs(pkg_mngrs, pkg_groups, no_upgrade)

        elif step in ['neovim_setup', 'font_setup']:
            # import step's function from ide_setup.py in same directory
            import_module('onboardme.ide_setup', package=f'.{step}')
            func = getattr(ide_setup, step)
            func()

        elif step == 'sudo_setup':
            # if we're not running as root, kick off another process
            setup_sudo()

    if 'firewall_setup' in steps:
        configure_firewall(remote_host)

    print_manual_steps(OS)
    return True


if __name__ == '__main__':
    main()
