"""
help text functions for the onboardme cli
"""
# file for rich printing
import click
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
from os import environ

# custom local module
from .constants import (DEFAULT_PKG_GROUPS, OPT_PKG_GROUPS, PKG_MNGRS, STEPS,
                        VERSION)


# this is for creating new help text svgs for the READMEs
RECORD = environ.get("OBM_SCREENSHOT", False)


def pretty_choices(default_list: list) -> str:
    """
    Takes a list of default choices and surrounds them with a meta markup tag
    and join them with a comma for a pretty return "Choices" string.
    Example: pretty_choices(['beep', 'boop']) returns:
             'Choices: [meta]beep[/meta], [meta]boop[/meta]'
    """
    defaults = '[/meta], [meta]'.join(default_list)
    return 'Choices: [meta]' + defaults + '[/meta]'


def options_help() -> dict:
    """
    Help text for all the options/switches for main()
    """
    dot_file_url = '[meta]https://github.com/jessebot/dot_files[/meta]'
    step_choices = pretty_choices(STEPS)
    pkg_mngr_choices = pretty_choices(PKG_MNGRS)
    logging_choices = pretty_choices(['debug', 'info', 'warn', 'error'])
    pkg_group_choices = pretty_choices(DEFAULT_PKG_GROUPS + OPT_PKG_GROUPS)

    return {
        'steps':
        f'[b]Only[/b] run [meta]STEP[/] in the script.\n{step_choices}\nExampl'
        'e: [switch]-s[/] [meta]dot_files[/] [switch]-s[/] [meta]packages',

        'git_url':
        f'A git repo URL for your dot files. Default: {dot_file_url}',

        'git_branch':
        'Branch to use for the git repo url. Default: main',

        'git_config_dir':
        'Directory to store the git configuration for your dot files. '
        'Default: ~/.config/dot_files',

        'generate_screenshot':
        'Generate a few SVGs for use in the docs and README. Undocumented.',

        'overwrite':
        '[b]Overwrites[/b] existing dot files with files from configured '
        "[option]--git_url[/option] repo. If you've set overwrite: true in "
        'your config, then --overwrite on the command line will act as a '
        'toggle, so it will NOT overwrite your dot files.',

        'pkg_managers':
        f'Specific [meta]PKG_MANAGER[/] to run. {pkg_mngr_choices}'
        '\nExample: [switch]-p[/] [meta]brew[/] [switch]-p[/] [meta]pip3.12',

        'pkg_groups':
        f"Package groups to install.\n{pkg_group_choices}\nExample:"
        " [switch]-g[/] [meta]devops[/] [switch]-g[/switch] [meta]gaming",

        'no_upgrade':
        "Do not upgrade the existing brew or apt packages.",

        'remote_host':
        'Setup SSH on a random port & add [meta]IP_ADDR[/] to firewall',

        'firewall':
        'Setup iptables (on [i]linux[/] only).',

        'version':
        f'Print the version of onboardme ({VERSION})',

        'log_level':
        f'Logging level. {logging_choices}\nDefault: [meta]warn[/meta]',

        'log_file':
        'Full path to file to log to, if set.',

        'quiet':
        "unstable. Don't output to stdout. "

    }


class RichCommand(click.Command):
    """
    Override Clicks help with a Richer version.

    This is from the Textualize/rich-cli project on github.com:
    https://github.com/Textualize/rich-cli
    """

    def format_help(self, ctx, formatter):

        class OptionHighlighter(RegexHighlighter):
            highlights = [r"(?P<switch>\-\w)",
                          r"(?P<option>\-\-[\w\-]+)",
                          r"(?P<unstable>[b][e][t][a])"]

        highlighter = OptionHighlighter()

        console = Console(theme=Theme({"option": "cornflower_blue",
                                       "switch": "deep_sky_blue1",
                                       "meta": "light_steel_blue",
                                       "unstable": "italic cyan"}),
                          highlighter=highlighter, record=RECORD)

        title = "☁️  [cornflower_blue]OnBoard[i]Me[/] 💻\n"
        desc = (
            "[steel_blue]Get your daily driver just the way you like it, from "
            "[b]text[/] [i]formatting[/], and dot files to opensource package "
            "installation, onboardme intends to save you time with "
            "initializing or upgrading your environment.")

        console.print(title + desc, justify="center")

        console.print("\n[b]Usage[/]:  [royal_blue1]onboardme[/] " +
                      "[cornflower_blue][OPTIONS]\n")

        options_table = Table(highlight=True, box=None, show_header=False,
                              row_styles=["", "dim"],
                              padding=(1, 1, 0, 0))

        # this used to be self.get_params(ctx)[1:] to have only one hidden option
        for param in self.get_params(ctx):

            if len(param.opts) == 2:
                opt1 = highlighter(param.opts[1])
                opt2 = highlighter(param.opts[0])
            else:
                opt2 = highlighter(param.opts[0])
                opt1 = Text("")

            if param.metavar:
                opt2 += Text(f" {param.metavar}",
                             style="meta")

            options = Text(" ".join(reversed(param.opts)))
            help_record = param.get_help_record(ctx)
            if help_record is None:
                help = ""
            else:
                help = Text.from_markup(param.get_help_record(ctx)[-1],
                                        emoji=False)

            if param.metavar:
                options += f" {param.metavar}"

            options_table.add_row(opt1, opt2, highlighter(help))

        url = (" ♥ docs: [link=https://jessebot.github.io/onboardme/]"
               "jessebot.github.io/onboardme[/link]")

        console.print(Panel(options_table,
                            border_style="dim light_steel_blue",
                            title="⌥  Options",
                            title_align="left",
                            subtitle=url,
                            subtitle_align="right"))

        # I use this to print a pretty svg at the end sometimes
        if RECORD:
            console.save_svg("docs/onboardme/screenshots/help_text.svg", title="term")
