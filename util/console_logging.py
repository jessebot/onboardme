#!/usr/bin/env python3.10
# this is for rich text, to pretty print things
from rich.console import Console
from rich.panel import Panel


CONSOLE = Console()


def print_panel(content='', title_txt='', title_alignment='center',
                border_style="white"):
    """
    prints content text in a box with title_txt
    """
    print('')

    panel = Panel(content, title=title_txt, title_align=title_alignment,
                  border_style=border_style)

    CONSOLE.print(panel)


def print_header(title='', line_style='royal_blue1'):
    """
    prints text centered in a line that spans the terminal
    """
    print('')

    CONSOLE.rule(title, style=line_style)


def print_msg(text='', alignment='center'):
    """
    prints text centered in the width of the terminal
    """

    CONSOLE.print(text, justify=alignment)
