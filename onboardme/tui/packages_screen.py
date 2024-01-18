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

    BINDINGS = [
            Binding(key="b,escape,q",
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
                    description="Next")
            ]

    ToggleButton.BUTTON_INNER = '♥'

    def __init__(self, config: dict, highlighted_package: str = "") -> None:
        # show the footer at bottom of screen or not
        self.show_footer = self.app.cfg['tui']['show_footer']

        # should be the packages section of onboardme config
        self.cfg = config

        # this changes depending on the list selected
        self.pkg_mnger = 'brew'

        # this is state storage
        self.previous_package = ''

        # inital highlight if we got here via a link
        self.initial_package = highlighted_package

        super().__init__()

    def compose(self) -> ComposeResult:
        """
        Compose package with for package input content
        """
        # header to be cute
        yield Header()

        # Footer to show keys
        footer = Footer()
        if not self.show_footer:
            footer.display = False
        yield footer

        selection_lists = {}
        for package_mngr in ['brew', 'pip3.11']:
            full_list = []
            for package in self.cfg[package_mngr]['packages']['default']:
                item = Selection(package.replace("_","-"), package, True)
                full_list.append(item)

            selection_list = SelectionList[str](
                    *full_list,
                    classes='selection-list-of-packages',
                    id=f'{package_mngr}-selection-list-of-packages'
                    )
            selection_lists[package_mngr] = selection_list

        with Container(id="packages-config-container"):
            # SelectionLists of k8s packagelications
            for package_mngr, selection_list in selection_lists.items():
                with Grid(classes="left-packages-container"):
                    with VerticalScroll(classes="select-add-packages",
                                        id=f"select-add-{package_mngr}-packages"):
                        yield selection_list

            # Bottom half of the screen for select-packages
            with VerticalScroll(id="package-notes-container"):
                yield Label("", id="package-description")

    def on_mount(self) -> None:
        """
        screen and box border styling
        """
        self.title = "ʕ ᵔᴥᵔʔ onboardme"
        sub_title = "Packages Configuration"
        self.sub_title = sub_title

        for package_mngr in ['brew', 'pip3.11']:
            # select-packages styling - select packages container - top left 
            select_packages_widget = self.get_widget_by_id(
                    f"select-add-{package_mngr}-packages"
                    )
            select_packages_widget.border_title = (
                    f"[#ffaff9]♥[/] [i]select[/] {package_mngr} [#C1FF87]packages"
                    )
            select_packages_widget.border_subtitle = (
                    f"[@click=screen.launch_new_package_modal()]"
                    f"✨ [i]new[/] {package_mngr} [#C1FF87]package[/][/]"
                    )

        if self.app.speak_screen_titles:
            # if text to speech is on, read screen title
            self.app.action_say(
                    "Screen title: Packages Configuration. Here you can select "
                    "which packages to install per package manager. On the left"
                    " is a list of packages for brew."
                    )

        # scroll down to specific app if requested
        if self.initial_package:
            self.scroll_to_package(self.initial_package)

    def action_launch_new_package_modal(self,
                                        package_manager: str) -> None:
        def get_new_package(package_response):
            package_manager = package_response[0]
            package_name = package_response[1]
            package_description = package_response[2]

            if package_name and package_description:
                self.create_new_package_in_yaml(package_manager,
                                                package_name,
                                                package_description)

        packages = self.cfg[package_manager]['packages']['default']
        self.app.push_screen(NewPackageModalScreen(packages, package_manager),
                             get_new_package)

    def scroll_to_package(self, package_manager: str, package_to_highlight: str) -> None:
        """ 
        lets you scroll down to the exact package you need in the package selection list
        """
        # get the packages selection list
        packages = self.query_one(SelectionList)

        # get the package name for the highlighted index
        highlight_package = packages.get_option_at_index(packages.highlighted).value

        # while the highlighted package is not package_to_highlight, keep scrolling
        while highlight_package != package_to_highlight:
            packages.action_cursor_down()
            highlight_package = packages.get_option_at_index(packages.highlighted).value

    @on(SelectionList.SelectionHighlighted)
    def update_highlighted_package_view(self,
                                        event: SelectionList.SelectionHighlighted) -> None:
        selection_list = self.get_widget_by_id(f"{self.pkg_mnger}-selection-list-of-packages")

        # only the highlighted index
        highlighted_idx = selection_list.highlighted

        # the actual highlighted package
        highlighted_package = selection_list.get_option_at_index(highlighted_idx).value

        if self.app.speak_on_focus:
            self.app.action_say(f"highlighted package is {highlighted_package}")

        # update the bottom app description to the highlighted_app's description
        blurb = format_description("test")
        self.get_widget_by_id('package-description').update(blurb)

        # styling for the select-packages - configure packages container - right
        package_title = highlighted_package.replace("_", " ").title()

        # select-packages styling - bottom
        package_desc = self.get_widget_by_id("package-notes-container")
        package_desc.border_title = f"📓 {package_title} [i]notes[/i]"

        self.previous_package = highlighted_package

    @on(SelectionList.SelectionToggled)
    def update_selected_packages(self,
                                 event: SelectionList.SelectionToggled) -> None:
        """ 
        when a selection list item is checked or unchecked, update the base package yaml
        """
        selection_list = event
        package = selection_list.get_option_at_index(event.selection_index).value
        if package in selection_list.selected:
            self.app.pkgs['brew']['packages']['default'][package]['enabled'] = True
        else:
            self.app.pkgs['brew']['packages']['default'][package]['enabled'] = False

        self.app.write_yaml()

    def create_new_package_in_yaml(self,
                                   package_manager: str,
                                   package_name: str,
                                   package_description: str = "") -> None:
        """ 
        add a new package to the packages yaml
        """
        underscore_name = package_name.replace(" ", "_").replace("-", "_")

        # updates the base user yaml
        self.app.pkgs['brew']['packages']['default'] = {
            "enabled": True,
            "description": package_description,
            }

        # adds selection to the app selection list
        packages = self.app.query_one(".selection-list-of-packages")
        packages.add_option(Selection(underscore_name.replace("_", "-"),
                                  underscore_name, True))

        # scroll down to the new app
        packages.action_last()
