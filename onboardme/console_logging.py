# this is for rich text, to pretty print things
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme


CONSOLE = Console(theme=Theme({"warn": "bold yellow",
                               "grn": "medium_spring_green",
                               "ohno": "magenta",
                               "header": "cornflower_blue"}))


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


def print_panel(content='', title_txt='', title_alignment='center',
                border_style="light_steel_blue"):
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
    CONSOLE.rule('[cornflower_blue]' + title, style=line_style)
    return


def print_sub_header(title='', style='light_steel_blue', alignment='center'):
    """
    prints text centered in a line that spans the terminal
    """
    print('')
    CONSOLE.print(title, style=style, justify='center')
    return


def print_msg(text='', alignment='center', style='dim italic'):
    """
    prints text centered in the width of the terminal
    """
    CONSOLE.print(text, justify=alignment, style=style)
    return
