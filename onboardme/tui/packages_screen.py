#!/usr/bin/env python3.11
# onboardme libraries
from onboardme.tui.package_widgets.new_package_modal import NewPackageModalScreen
from onboardme.tui.package_widgets.package_search_widget import PackageSearch

# external libraries
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll, Grid
from textual.screen import Screen
from textual.widgets import Footer, Header, OptionList, Collapsible
from textual.widgets.option_list import Option, Separator
from textual.widgets._toggle_button import ToggleButton


class PackagesConfig(Screen):
    """
    Textual screen for onboardme packages
    """
    CSS_PATH = ["./css/packages_config.tcss",
                "./css/package_info.tcss"]

    BINDINGS = [
            Binding(key="b,escape,q",
                    key_display="b",
                    action="app.pop_screen",
                    description="Back"),
            Binding(key="n",
                    key_display="n",
                    action="app.request_onboardme_cfg",
                    description="Next"),
            ]

    ToggleButton.BUTTON_INNER = '♥'

    def __init__(self, config: dict, highlighted_package: str = "") -> None:
        # show the footer at bottom of screen or not
        self.show_footer = self.app.cfg['tui']['show_footer']

        # should be the packages section of onboardme config
        self.cfg = config

        # this changes depending on the list selected
        self.pkg_mngr = ''

        # this changes depending on the list selected
        self.pkg_group = 'default'

        # this is state storage
        self.package = ''

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

                        option_list = OptionList(
                                *full_list,
                                id=f"{package_mngr}-{package_group}-list-of-packages",
                                classes=f"list-of-packages {package_mngr} {package_group}"
                                )
                        option_lists[package_mngr][package_group] = option_list

        # full packages screen
        with Grid(id="packages-screen"):
            # all the package manager lists
            with Grid(id="packages-config-container",
                      classes="packages-large-grid"):
                # Bottom half of the screen for notes on a given package
                with Grid(id="package-notes-container"):
                    yield PackageSearch(self.cfg,
                                        self.pkg_mngr,
                                        id="package-search-widget")

                # each package manager and it's groups
                for package_mngr, package_groups in option_lists.items():
                    with Grid(classes="packages-column"):
                        with VerticalScroll(classes="select-add-packages",
                                            id=f"select-add-{package_mngr}-packages"):
                            for package_group, packages_list in package_groups.items():
                                with Collapsible(collapsed=False,
                                                 title=package_group):
                                    yield packages_list

    def on_mount(self) -> None:
        """
        screen and box border styling
        """
        self.title = "ʕ ᵔᴥᵔʔ onboardme"
        sub_title = "Packages Configuration"
        self.sub_title = sub_title

        for package_mngr in self.cfg.keys():
            # select-packages styling - select packages container - top left 
            select_packages_widget = self.get_widget_by_id(
                    f"select-add-{package_mngr}-packages"
                    )
            emoji = self.cfg[package_mngr]['emoji']
            select_packages_widget.border_title = (
                    f"{emoji} [i][#C1FF87]{package_mngr}[/]"
                    )

        for option_list in self.query(".list-of-packages"):
            option_list.highlighted = None

        if self.app.speak_screen_titles:
            # if text to speech is on, read screen title
            self.app.action_say(
                    "Screen title: Packages Configuration. Here you can select "
                    "which packages to install per package manager."
                    )

        # scroll down to specific app if requested
        if self.initial_package:
            self.scroll_to_package(self.initial_package)

        # select-packages styling - bottom
        package_desc = self.get_widget_by_id("package-notes-container")
        package_desc.border_title = "🔎 [i]Search for package[/]"

    @on(OptionList.OptionSelected)
    def update_highlighted_package_view(self,
                                        event: OptionList.OptionSelected) -> None:
        olist = event.option_list
        if isinstance(olist, OptionList) and "list-of-packages" in olist.classes:
            search_widget = self.get_widget_by_id("package-search-widget")

            # the actual highlighted package
            highlighted_package = event.option

            if self.app.speak_on_focus:
                self.app.action_say(f"highlighted package is {highlighted_package}")

            # description
            classes = olist.id.split('-')
            manager = classes[0]
            # group = classes[1]

            # blurb_txt = (f"group: [#ffaff9]{group}[/]")
            # # update the bottom app description to the highlighted_app's description
            # blurb = format_description(blurb_txt)
            # self.get_widget_by_id('package-description').update(blurb)

            self.package = highlighted_package.prompt
            self.pkg_mngr = manager

            # update the input for the package search
            search_widget.action_update_package_and_manager(highlighted_package.prompt,
                                                            [manager])

    def action_install_package(self) -> None:
        """
        install the package
        """
        def process_output(output):
            print("made it output 💪")
            # self.action_add_package_in_yaml(self.cfg,
            #                                 self.pkg_mngr,
            #                                 self.pkg_group,
            #                                 self.package)

        self.app.push_screen(NewPackageModalScreen(self.cfg,
                                                   self.pkg_mngr,
                                                   self.pkg_group,
                                                   self.package),
                             process_output)
        

    def action_add_package_in_yaml(self,
                            package_manager: str,
                            package_group: str,
                            package: str) -> None:
        """ 
        add a new package to the packages yaml
        """
        # updates the base user yaml
        if package not in self.app.pkgs[package_manager]['packages'][package_group]:
            self.app.pkgs[package_manager]['packages'][package_group].append(package)

        # adds selection to the app selection list
        packages_list = self.get_widget_by_id(
                f"{package_manager}-{package_group}-list-of-packages"
                )
        packages_list.add_option(package.replace("_","-"))

    def action_remove_package(self,
                              package_manager: str,
                              package_group: str,
                              package: str) -> None:
        """
        remove a package from config and uninstall it
        """
        # updates the base user yaml
        if package in self.app.pkgs[package_manager]['packages'][package_group]:
            idx = self.app.pkgs[package_manager]['packages'][package_group].index(package)
            self.app.pkgs[package_manager]['packages'][package_group].pop(idx)

        # adds selection to the app selection list
        packages_list = self.get_widget_by_id(
                f"{package_manager}-{package_group}-list-of-packages"
                )
        packages_list.remove_option(package.replace("_","-"))

    def scroll_to_package(self,
                          package_manager: str, 
                          package_group: str,
                          package_to_highlight: str) -> None:
        """ 
        lets you scroll down to the exact package you need in the package selection list
        """
        # get the packages selection list
        packages = self.get_widget_by_id(
                f"{package_manager}-{package_group}-list-of-packages"
                )

        # get the package name for the highlighted index
        highlight_package = packages.highlighted_child

        # while the highlighted package is not package_to_highlight, keep scrolling
        while highlight_package != package_to_highlight:
            packages.action_cursor_down()
            highlight_package = packages.highlighted