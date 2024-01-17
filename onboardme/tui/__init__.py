from onboardme.tui.base import BaseApp
from onboardme.console_logging import print_msg
import sys


def launch_config_tui(cfg: dict, packages: dict):
    """
    Run all the TUI screens
    """
    config = BaseApp(cfg, packages).run()

    if not config:
        print_msg("[blue]♥[/] [cyan]Have a nice day[/] [blue]♥\n", style="italic")
        sys.exit()

    return config
