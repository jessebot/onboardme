#!/usr/bin/env python3.11
# onboardme libraries
from onboardme.tui.package_widgets.new_package_modal import NewPackageModalScreen
from onboardme.tui.util import format_description

# external libraries
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll, Container, Grid
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, SelectionList
from textual.widgets._toggle_button import ToggleButton
from textual.widgets.selection_list import Selection


class PackagesConfig(Screen):
    """
    Textual app to onboardme applications
    """
    CSS_PATH = ["./css/packages_config.tcss"]

    BINDINGS = [Binding(key="b,escape,q",
                        key_display="b",
                        action="app.pop_screen",
                        description="Back"),
                Binding(key="a",
                        key_display="a",
                        action="screen.launch_new_package_modal",
                        description="New Package"),
                Binding(key="n",
                        key_display="n",
                        action="app.request_onboardme_cfg",
                        description="Next")]

    ToggleButton.BUTTON_INNER = '♥'

    def __init__(self, config: dict, highlighted_app: str = "") -> None:
        # show the footer at bottom of screen or not
        self.show_footer = self.app.cfg['tui']['show_footer']

        # should be the apps section of onboardme config
        self.cfg = config

        # this is state storage
        self.previous_app = ''

        # inital highlight if we got here via a link
        self.initial_app = highlighted_app

        super().__init__()

    def compose(self) -> ComposeResult:
        """
        Compose app with for app input content
        """
        # header to be cute
        yield Header()

        # Footer to show keys
        footer = Footer()
        if not self.show_footer:
            footer.display = False
        yield footer

        full_list = []
        for package in self.cfg['brew']['packages']['default']:
            item = Selection(package.replace("_","-"), package, True)
            full_list.append(item)

        selection_list = SelectionList[str](*full_list,
                                            id='selection-list-of-apps')

        with Container(id="apps-config-container"):
            # top left: the SelectionList of k8s applications
            with Grid(id="left-apps-container"):
                with VerticalScroll(id="select-add-apps"):
                    yield selection_list

            # top right: vertically scrolling container for all inputs
            yield VerticalScroll(id='package-inputs-pane')

            # Bottom half of the screen for select-apps
            with VerticalScroll(id="package-notes-container"):
                yield Label("", id="package-description")

    def on_mount(self) -> None:
        """
        screen and box border styling
        """
        self.title = "ʕ ᵔᴥᵔʔ onboardme"
        sub_title = "Packages Configuration"
        self.sub_title = sub_title

        # select-apps styling - select apps container - top left 
        select_apps_widget = self.get_widget_by_id("select-add-apps")
        select_apps_widget.border_title = "[#ffaff9]♥[/] [i]select[/] [#C1FF87]packages"
        select_apps_widget.border_subtitle = "[@click=screen.launch_new_package_modal]✨ [i]new[/] [#C1FF87]package[/][/]"

        if self.app.speak_screen_titles:
            # if text to speech is on, read screen title
            self.app.action_say(
                    "Screen title: Packages Configuration."
                    "Here you can select which packages to install per package manager."
                    " On the left is a list of packages for brew."
                    )

        # scroll down to specific app if requested
        if self.initial_app:
            self.scroll_to_app(self.initial_app)

    def action_launch_new_package_modal(self) -> None:
        def get_new_app(package_response):
            package_name = package_response[0]
            package_description = package_response[1]

            if package_name and package_description:
                self.create_new_package_in_yaml(package_name, package_description)

        self.app.push_screen(NewPackageModalScreen(["argo-cd"]), get_new_app)

    def scroll_to_app(self, package_to_highlight: str) -> None:
        """ 
        lets you scroll down to the exact app you need in the app selection list
        """
        # get the apps selection list
        apps = self.query_one(SelectionList)

        # get the app name for the highlighted index
        highlight_app = apps.get_option_at_index(apps.highlighted).value

        # while the highlighted app is not package_to_highlight, keep scrolling
        while highlight_app != package_to_highlight:
            apps.action_cursor_down()
            highlight_app = apps.get_option_at_index(apps.highlighted).value

    @on(SelectionList.SelectionHighlighted)
    def update_highlighted_package_view(self) -> None:
        selection_list = self.query_one(SelectionList)

        # only the highlighted index
        highlighted_idx = selection_list.highlighted

        # the actual highlighted app
        highlighted_app = selection_list.get_option_at_index(highlighted_idx).value

        if self.app.speak_on_focus:
            self.app.action_say(f"highlighted app is {highlighted_app}")

        # update the bottom app description to the highlighted_app's description
        blurb = format_description("test")
        self.get_widget_by_id('package-description').update(blurb)

        # styling for the select-apps - configure apps container - right
        package_title = highlighted_app.replace("_", " ").title()
        package_cfg_title = f"🔧 [i]configure[/] parameters for [#C1FF87]{package_title}"
        self.get_widget_by_id("package-inputs-pane").border_title = package_cfg_title

        # select-apps styling - bottom
        package_desc = self.get_widget_by_id("package-notes-container")
        package_desc.border_title = f"📓 {package_title} [i]notes[/i]"

        self.previous_app = highlighted_app

    @on(SelectionList.SelectionToggled)
    def update_selected_apps(self, event: SelectionList.SelectionToggled) -> None:
        """ 
        when a selection list item is checked or unchecked, update the base app yaml
        """
        selection_list = self.query_one(SelectionList)
        app = selection_list.get_option_at_index(event.selection_index).value
        if app in selection_list.selected:
            self.app.cfg['apps'][app]['enabled'] = True
        else:
            self.app.cfg['apps'][app]['enabled'] = False

        self.app.write_yaml()

    def create_new_package_in_yaml(self, package_name: str, package_description: str = "") -> None:
        underscore_name = package_name.replace(" ", "_").replace("-", "_")

        # updates the base user yaml
        self.app.cfg['apps'][underscore_name] = {
            "enabled": True,
            "description": package_description,
            }

        # adds selection to the app selection list
        apps = self.app.get_widget_by_id("selection-list-of-apps")
        apps.add_option(Selection(underscore_name.replace("_", "-"),
                                  underscore_name, True))

        # scroll down to the new app
        apps.action_last()
