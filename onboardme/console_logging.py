from itertools import zip_longest
from os import getenv
# this is for rich text, to pretty print things
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme

CONSOLE = Console(theme=Theme({"warn": "bold yellow",
                               "grn": "medium_spring_green",
                               "ohno": "magenta",
                               "header": "cornflower_blue"}))


def print_panel(content='', title_txt='', title_alignment='center',
                border_style="light_steel_blue1"):
    """
    prints text in a box with a light_steel_blue1 border and title_txt
    """
    print('')
    panel = Panel(content, title=title_txt, title_align=title_alignment,
                  border_style=border_style)
    CONSOLE.print(panel)
    return


def print_header(title='', line_style='royal_blue1'):
    """
    prints text centered in a line that spans the terminal
    """
    print('')
    CONSOLE.rule(title, style=line_style)
    return


def print_msg(text='', alignment='center'):
    """
    prints text centered in the width of the terminal
    """
    CONSOLE.print(text, justify=alignment)
    return


def print_git_file_table(remote_git_files=[], file_verb="", branch="",
                         git_url=""):
    """
    Takes a list of files and pretty prints them in a nice table in 2 columns:
        remote_git_files - [], list of files to print in 2 columns
        file_verb        - "", what is their relation to the origin/{branch}
        branch           - "", git branch we're looking at
        git_url          - "", url of git repo we're working with
    """
    emote = "[header]ʕ ･ᴥ･ʔ[/header][sky_blue1]"
    if "differ" in file_verb:
        emote = "[yellow]:warning: ʕ ⚈ᴥ⚈ʔ"
    # table to print the results of all the files
    table = Table(expand=True,
                  box=box.MINIMAL_DOUBLE_HEAD,
                  row_styles=["", "dim"],
                  border_style="dim",
                  show_header=False)
    table.add_column(" ", style="green")

    # remove all trailing space and then create a list of file paths
    home_dir = getenv("HOME")
    files = remote_git_files.rstrip().replace("../..", home_dir).split('\n')
    if len(files) < 2:
        table.add_row(files[0])
    else:
        table.add_column(" ", style="green")

        # find midpoint of the list. if it's a float (e.g. 20.5) convert to int
        mid = int(len(files) / 2)
        # iterate over both halfs of list till the end of the longest list,
        for (f1, f2) in zip_longest(files[0:mid], files[mid:], fillvalue=" "):
            if f1 != " " and f2 != " ":
                table.add_row(f1, f2)
            else:
                table.add_row(f2, " ")

    git_repo = "[/grn]/[grn]".join(git_url.split('/')[-2:]).replace(".git", "")
    msg = (f"{emote} The following file(s) {file_verb} [grn]"
           f"origin[/grn]/[grn]{branch}[/grn] in [grn]{git_repo}")
    print_panel(table, msg, "left")
    return
