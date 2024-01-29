# onboardme libraries
from onboardme.constants import (XDG_CONFIG_FILE, XDG_CONFIG_DIR, 
                                 INITIAL_USR_CONFIG, load_cfg)
from onboardme.tui.packages_screen import PackagesConfig
from onboardme.tui.help_screen import HelpScreen
from onboardme.tui.tui_config_screen import TuiConfigScreen

# external libraries
from os import system
from pyfiglet import Figlet
from rich.text import Text
from ruamel.yaml import YAML
from textual import on
from textual.app import App, ComposeResult
from textual.events import DescendantFocus
from textual.binding import Binding
from textual.containers import Grid
from textual.widgets import (Footer, Button, DataTable, Input, Label,
                             Switch, Select)

# list of approved words for nouns
CUTE_NOUNS = [
        "bunny", "hoglet", "puppy", "kitten", "knuffel", "friend", "egel",
        "meerkoet", "raccoon", "wasbeertje"
        ]

CUTE_ADJECTIVE = [
        "lovely", "adorable", "cute", "friendly", "nice", "leuke", "mooie", 
        "vriendelijke", "cool", "soft", "smol", "small", "klein"
        ]

class BaseApp(App):
    BINDINGS = [
            Binding(key="?,h",
                    key_display="?",
                    action="request_help",
                    description="Help",
                    show=True),
            Binding(key="c",
                    key_display="c",
                    action="request_config",
                    description="Config"),
            Binding(key="n",
                    key_display="n",
                    action="request_apps_cfg",
                    description="next"),
            Binding(key="f",
                    key_display="f",
                    action="toggle_footer",
                    description="Toggle footer"),
            Binding(key="q,escape",
                    action="quit",
                    show=False),
            Binding(key="f5",
                    key_display="f5",
                    description="Speak",
                    action="app.say",
                    show=True)
            ]

    CSS_PATH = ["./css/base.tcss",
                "./css/help.tcss"]

    def __init__(self, user_config: dict, packages: dict) -> None:
        self.cfg = user_config
        self.pkgs = packages
        self.show_footer = self.cfg['tui']['show_footer']
        self.cluster_names = []
        self.current_cluster = ""
        self.sensitive_values = {
                'nextcloud': {},
                'matrix': {},
                'mastodon': {},
                'zitadel': {}
                }

        # configure global accessibility
        accessibility_opts = self.cfg['tui']['accessibility']
        tts = accessibility_opts['text_to_speech']
        self.speak_on_focus = tts['on_focus']
        self.speak_screen_titles = tts['screen_titles']
        self.speak_on_key_press = tts['on_key_press']
        self.speech_program = tts['speech_program']
        self.bell_on_focus = accessibility_opts['bell']['on_focus']
        self.bell_on_error = accessibility_opts['bell']['on_error']
        super().__init__()

    def compose(self) -> ComposeResult:
        """
        Compose app with screens
        """
        # Footer to show keys
        footer = Footer()

        if not self.show_footer:
            footer.display = False
        yield footer

        # full screen container
        with Grid(id="base-screen-container"):
            yield Label(Figlet(font="standard").renderText("onboardme"),
                        id="onboardme-header")

    def on_mount(self) -> None:
        """
        screen and box border styling
        """
        if self.speak_screen_titles:
            self.action_say(
                    "Welcome to onboardme. Press tab, then C, to configure "
                    "accessibility options."
                    )

    def action_request_apps_cfg(self, app_to_highlight: str = "") -> None:
        """
        launches the argo app config screen
        """
        if app_to_highlight:
            self.app.push_screen(PackagesConfig(self.pkgs, app_to_highlight))
        else:
            self.app.push_screen(PackagesConfig(self.pkgs, ""))

    def action_request_confirm(self) -> None:
        """
        show confirmation screen
        """
        self.app.push_screen(ConfirmConfig(self.cfg))

    def action_request_help(self,) -> None:
        """
        if the user presses 'h' or '?', show the help modal screen
        """
        self.push_screen(HelpScreen())

    def action_request_config(self,) -> None:
        """ 
        if the user pressed 'c', show the TUI config screen
        """
        self.push_screen(TuiConfigScreen(self.cfg['tui']))

    def action_toggle_footer(self) -> None:
        """
        don't display the footer, or do 🤷
        """
        footer = self.query_one(Footer)

        if footer.display:
            footer.display = False
            self.notify(
                "\n✨ Press [gold3]f[/] to re-enable the footer",
                timeout=9,
                title="Footer disabled"
            )
            self.cfg['tui']['show_footer'] = False
        else:
            footer.display = True
            self.cfg['tui']['show_footer'] = True

    def write_yaml(self,
                   config_file: str = f"{XDG_CONFIG_DIR}{XDG_CONFIG_FILE}") -> None:
        """
        dump current self.cfg to user's onboardme config.yaml
        """
        yaml = YAML()

        with open(config_file, 'w') as onboardme_config:
            yaml.dump(self.cfg, onboardme_config)

    def action_say(self, text_for_speech: str = "") -> None:
        """ 
        Use the configured speech program to read a string aloud. If no string
        is passed in, and self.speak_on_key_press is True, we read the currently
        focused element id
        """
        say = self.speech_program
        if text_for_speech:
            text_for_speech = text_for_speech.replace("(", "").replace(")", "")
            text_for_speech = text_for_speech.replace("[i]", "").replace("[/]", "")
            system(f"{say} {text_for_speech}")

        elif not text_for_speech:
            # if the use pressed f5, the key to read the widget id aloud
            if self.speak_on_key_press:
                focused = self.app.focused
                system(f"{say} element is {focused.id}")

                # if it's a data table, read out the row content
                if isinstance(focused, DataTable):
                    self.say_row(focused)

    def say_row(self, data_table: DataTable) -> None:
        """
        get the column names and row content of a DataTable and read aloud
        """
        row_index = data_table.cursor_row
        row = data_table.get_row_at(row_index)
        # get the row's first column and remove whitespace
        row_column1 = row[0].plain.strip()
        # change ? to question mark so it reads aloud well
        if row_column1 == "?":
            row_column1 = "question mark"
        row_column2 = row[1].plain.strip()

        # get the column names
        columns = list(data_table.columns.values())
        column1 = columns[0].label
        column2 = columns[1].label

        system(f"{self.speech_program} Selected {column1}: {row_column1}."
               f" {column2}: {row_column2}")

    @on(DescendantFocus)
    def on_focus(self, event: DescendantFocus) -> None:
        """ 
        on focus, say the id of each element and the value or label if possible
        """
        if self.speak_on_focus:
            id = event.widget.id
            self.action_say(f"element is {id}")

            # input fields
            if isinstance(event.widget, Input):
                content = event.widget.value
                placeholder = event.widget.placeholder
                if content:
                    self.action_say(f"value is {content}")
                elif placeholder:
                    self.action_say(f"place holder text is {placeholder}")

            # buttons
            elif isinstance(event.widget, Button):
                self.action_say(f"button text is {event.widget.label}")

            # switches
            elif isinstance(event.widget, Switch) or isinstance(event.widget, Select):
                self.action_say(f"value is {event.widget.value}")

            # also read the tooltip if there is one
            tooltip = event.widget.tooltip
            if tooltip:
                self.action_say(f"tooltip is {tooltip}")

        if self.bell_on_focus:
            self.app.bell()

    def check_for_invalid_inputs(self, apps_dict: dict = {}) -> list:
        """
        check each app for any empty init or secret key fields
        """
        invalid_apps = {}

        if apps_dict:
            for app, metadata in apps_dict.items():
                if not metadata['enabled']:
                    continue

                empty_fields = []

                # check for empty init fields (some apps don't support init at all)
                init_dict = metadata.get('init', None)
                if init_dict:
                    # make sure init is enabled before checking
                    if init_dict['enabled']:
                        # regular yaml inputs
                        init_values = init_dict.get('values', None)
                        if init_values:
                            for key, value in init_values.items():
                                if not value:
                                    empty_fields.append(key)

                        # sensitive inputs
                        init_sensitive_values = init_dict.get('sensitive_values', None)
                        if init_sensitive_values:
                            prompts = self.check_for_env_vars(app, metadata)
                            if prompts:
                                for value in prompts:
                                    if not self.sensitive_values[app].get(value, ""):
                                        empty_fields.append(value)

                # check for empty secret key fields (some apps don't have secret keys)
                secret_keys = metadata['argo'].get('secret_keys', None)
                if secret_keys:
                    for key, value in secret_keys.items():
                        if not value:
                            empty_fields.append(key)

                if empty_fields:
                    invalid_apps[app] = empty_fields

        return invalid_apps



if __name__ == "__main__":
    pkg_mngrs_list_of_dicts = load_cfg('packages.yml')
    app = BaseApp(INITIAL_USR_CONFIG, pkg_mngrs_list_of_dicts)
    app.run()
