#!/usr/bin/env python3.11
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Grid
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import Label, DataTable


class HelpScreen(ModalScreen):
    """
    dialog screen to show help text
    """
    BINDINGS = [
            Binding(key="?,q,escape",
                    key_display="q",
                    action="disable_help",
                    description="Exit Help Screen",
                    show=True),
            Binding(key="n",
                    show=False,
                    action="app.bell")
                ]

    def compose(self) -> ComposeResult:
        welcome = ("Use your 🐁 to click anything in the UI ✨ Or use the "
                   "following key bindings. For additional help, check out the "
                   "[steel_blue][link=https://small-hack.github.io/onboardme/]docs[/][/]")

        with Grid(id="help-container"):
            yield Label(welcome, classes="help-text")
            yield Grid(id="help-options")

    def on_mount(self) -> None:
        # styling for the select-apps tab - select apps container - left
        select_apps_title = ('[i]Welcome[/] to [steel_blue]'
                             '[link=https://github.com/jessebot/onboardme]'
                             'onboardme[/][/]')
        help_container = self.get_widget_by_id("help-container")
        help_container.border_title = select_apps_title
        help_container.border_subtitle = (
                "made with 💙 + 🐍 + [steel_blue][i][link="
                "https://github.com/Textualize/textual]textual[/][/][/]"
                )

        if self.app.speak_screen_titles:
            # if text to speech is on, read screen title
            self.app.action_say(
                    "Screen title: Help Screen. Use your mouse to click anything"
                    " in the UI ✨ Or use the following key bindings. For "
                    "additional help, checkout https://github.com/jessebot/onboadme"
                    )

        self.build_help_table()

    def build_help_table(self) -> None:
        data_table = DataTable(zebra_stripes=True,
                               id="help-table",
                               cursor_type="row")

        # then fill in the cluster table
        data_table.add_column(Text("Key Binding", justify="center"))
        data_table.add_column(Text("Description"))

        link_help = ("open link; terminal dependent, so meta can be shift,"
                     "\n option, windowsKey, command, or control")

        # tips for new/forgetful users (the maintainers are also forgetful <3)
        help_dict = {
                "➡ ": "complete suggestion in input field",
                "⬆/⬇": "navigate up and down the app selection list",
                "tab": "focus next element",
                "shift+tab": "focus previous element",
                "↩ enter": "save input and/or press button",
                "?,h": "toggle help screen",
                "spacebar": "select selection option",
                "meta+click": link_help,
                "escape,q": "leave current screen and go home",
                "c": "launch the config screen",
                "f5": "read aloud current focused element id",
                "f": "toggle showing the footer"
                }

        for key_binding, description in help_dict.items():
            # we use an extra line to center the rows vertically 
            styled_row = [
                    Text(str("\n" + key_binding)),
                    Text(str("\n" + description))
                          ]

            if key_binding == "meta+click":
                data_table.add_row(*styled_row, height=4, key=key_binding)
            else:
                # we add extra height to make the rows more readable
                data_table.add_row(*styled_row, height=3, key=key_binding)

        self.get_widget_by_id("help-options").mount(data_table)

    def action_disable_help(self) -> None:
        """
        if user presses '?', 'h', or 'q', we exit the help screen
        """
        self.app.pop_screen()
