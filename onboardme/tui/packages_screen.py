#!/usr/bin/env python3.11
# onboardme libraries
from onboardme.tui.package_widgets.new_package_modal import NewPackageModalScreen
from onboardme.tui.util import format_description

# external libraries
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll, Grid
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, OptionList, Collapsible, Select
from textual.widgets.option_list import Option, Separator
from textual.widgets._toggle_button import ToggleButton


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

        option_lists = {}
        # iterate through package managers
        for package_mngr, metadata in self.cfg.items():
            option_lists[package_mngr] = {}
            package_groups = metadata['packages'].items()
            # iterate through package groups
            for package_group, group_list in package_groups:
                full_list = []
                # iterate through packages in package groups
                if group_list:
                    for package in group_list:
                        option_str = package.replace("_","-")
                        full_list.append(Option(package, id=option_str))
                        full_list.append(Separator())

                        option_lists[package_mngr][package_group] = OptionList(
                                *full_list,
                                id=f"{package_mngr}-{package_group}-list-of-packages",
                                classes="list-of-packages"
                                )

        with Grid(id="packages-config-container",
                  classes="packages-large-grid"):
            # k8s packagelications
            for package_mngr, package_groups in option_lists.items():
                with Grid(classes="left-packages-container"):
                    package_managers = self.cfg.keys()
                    yield Select.from_values(package_managers,
                                             value=package_mngr)
                    with VerticalScroll(classes="select-add-packages",
                                        id=f"select-add-{package_mngr}-packages"):
                        for package_group, packages_list in package_groups.items():
                            with Collapsible(collapsed=False, title=package_group):
                                yield packages_list

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

        # for package_mngr in ['brew', 'pip3.11']:
        #     # select-packages styling - select packages container - top left 
        #     select_packages_widget = self.get_widget_by_id(
        #             f"select-add-{package_mngr}-packages"
        #             )
        #     # select_packages_widget.border_title = (
        #     #         f"[#ffaff9]♥[/] [i]{package_mngr}[/] [#C1FF87]packages"
        #     #         )
        #     select_packages_widget.border_subtitle = (
        #             f"[@click=screen.launch_new_package_modal()]"
        #             f"✨ [i]new[/] {package_mngr} [#C1FF87]package[/][/]"
        #             )

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

    def scroll_to_package(self,
                          package_manager: str, 
                          package_group: str,
                          package_to_highlight: str) -> None:
        """ 
        lets you scroll down to the exact package you need in the package selection list
        """
        # get the packages selection list
        packages = self.get_widget_by_id(f"{package_manager}-{package_group}-list-of-packages")

        # get the package name for the highlighted index
        highlight_package = packages.highlighted_child

        # while the highlighted package is not package_to_highlight, keep scrolling
        while highlight_package != package_to_highlight:
            packages.action_cursor_down()
            highlight_package = packages.highlighted

    @on(OptionList.OptionHighlighted)
    def update_highlighted_package_view(self,
                                        event: OptionList.OptionHighlighted) -> None:

        # the actual highlighted package
        highlighted_package = event.option

        if self.app.speak_on_focus:
            self.app.action_say(f"highlighted package is {highlighted_package}")

        # update the bottom app description to the highlighted_app's description
        blurb = format_description("test")
        self.get_widget_by_id('package-description').update(blurb)

        # styling for the select-packages - configure packages container - right
        package_title = highlighted_package

        # select-packages styling - bottom
        package_desc = self.get_widget_by_id("package-notes-container")
        package_desc.border_title = f"📓 {package_title} [i]notes[/i]"

        self.previous_package = highlighted_package

    def create_new_package_in_yaml(self,
                                   package_manager: str,
                                   package_group: str,
                                   package_name: str,
                                   package_description: str = "") -> None:
        """ 
        add a new package to the packages yaml
        """
        # updates the base user yaml
        if package_name not in self.app.pkgs[package_manager]['packages']['default']:
            self.app.pkgs[package_manager]['packages']['default'] = package_name


        # adds selection to the app selection list
        packages = self.get_widget_by_id(
                f"{package_manager}-{package_group}-list-of-packages"
                )
        packages.add_option(package_name.replace("_","-"))
