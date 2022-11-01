# this is for rich text, to pretty print things
from rich.console import Console
from rich.panel import Panel
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
