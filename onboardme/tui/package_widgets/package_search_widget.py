from onboardme.packages.search import search_for_package

from textual import on
from textual.app import ComposeResult
from textual.containers import Grid, VerticalScroll
from textual.events import Mount
from textual.validation import Length
from textual.widget import Widget
from textual.widgets import Input, Label, SelectionList, TabbedContent, TabPane
from textual.widgets.selection_list import Selection


class PackageSearch(Widget):
    """ 
    widget to search for packages for one or more package managers
    """
    CSS_PATH = ["../css/base_modal.tcss",
                "../css/package_info.tcss"]

    def __init__(self,
                 package_manager_configs: dict = {},
                 package_manager: list = None,
                 id: str = None) -> None:
        self.cfg = package_manager_configs
        if not package_manager:
            self.pkg_mngr = ["brew"]
        else:
            self.pkg_mngr = package_manager

        # if there's an id for this widget, respect it
        if id:
            super().__init__(id=id)
        else:
            super().__init__()

    def compose(self) -> ComposeResult:
        # create a small SelectionList of package managers
        selections = []
        for pkg_mgr in self.cfg.keys():
            selection_dict = {"prompt": pkg_mgr, "value": pkg_mgr,
                              "id": f"{pkg_mgr}-selection"}

            # if there's already a package selected
            if pkg_mgr in self.pkg_mngr:
                selection_dict["initial_state"] = True

            selections.append(Selection(**selection_dict))

        selection_list = SelectionList[str](*selections, id="pkg-mngr-list")
        selection_list.tooltip = "Package Managers to search"

        # create input for package to search for
        input = Input(validators=[Length(minimum=2)],
                      placeholder="📦 Name of package",
                      id="package-name-input")
        input.tooltip = "Name for your package in onboardme"

        # grid for pckage manager selection list and package search input
        with Grid(id="package-search-inputs"):
            yield selection_list
            yield input

        with VerticalScroll(id="pkg-info"):
            # default help text
            help = "[i]Search[/] for a package to display any info we can find about it."
            # Add the TabbedContent widget
            with TabbedContent(initial="brew"):
                for tab in self.screen.cfg.keys():
                    # take care of package managers with dots
                    clean_tab = tab.replace(".","-")
                    emoji = self.cfg[tab]['emoji']
                    emoji_tab = " ".join([emoji, tab])
                    with TabPane(emoji_tab, id=clean_tab):
                        # this gets updated based on user's search
                        yield Label(help,
                                    id=f"{clean_tab}-package-res",
                                    classes="package-res")

    def action_show_tab(self, tab: str) -> None:
        """Switch to a new tab."""
        self.get_child_by_type(TabbedContent).active = tab

    @on(Input.Submitted)
    def input_validation(self, event: Input.Submitted) -> None:
        """ 
        validate input on any text entered
        """
        if event.input.id == "package-name-input":
            if not event.validation_result.is_valid:
                # if result is not valid, notify the user why
                self.notify(
                        "\n".join(event.validation_result.failure_descriptions),
                        severity="warning",
                        title="⚠️ Input Validation Error\n")
                self.app.bell()

    @on(Mount)
    @on(SelectionList.SelectedChanged)
    def update_selected_view(self) -> None:
        """
        update self.pkg_mngr with currently selected package manager
        """
        self.pkg_mngr = self.get_widget_by_id("pkg-mngr-list").selected

    @on(Input.Submitted)
    def input_submitted(self, event: Input.Submitted) -> None:
        """ 
        validate input on text submitted and update res Label
        """
        self.search_for_package(event.value)

    def search_for_package(self, package: str) -> None:
        """
        search self.pkg_mngr for a given package
        """
        print(f"value for input submitted is {package}")
        pkg_mngr = self.pkg_mngr
        if isinstance(pkg_mngr, str):
            if pkg_mngr not in self.cfg.keys():
                pkg_mngr = self.cfg.keys()

        res = search_for_package(
                package=package,
                package_manager=self.pkg_mngr,
                cfg=self.cfg
                )

        # for multiple package manger results
        for package_manager, pkg_search_res in res.items():
            formatted_res = ""

            # if the result for a package manger search includes multiple packages
            if isinstance(pkg_search_res, list):
                joined_res = "\n".join(pkg_search_res['info']).replace('\n','\n\n')
                formatted_res += f"{package_manager}:\n{joined_res}"
            else:
                formatted_res += (
                        f"{pkg_search_res['info'].replace('\n','\n\n')}"
                        )

            # label to update for providing package info result
            clean_tab = package_manager.replace(".", "-")
            res_label = self.get_widget_by_id(f"{clean_tab}-package-res")
            res_label.update(formatted_res.lstrip())

        # create install button
        note_box = self.screen.get_widget_by_id("package-notes-container")

        # add all package mangers to the screen self cache
        self.screen.pkg_mngr = pkg_mngr

        installed = False
        emoji = "📦"
        # check if any of the package managers are used to install the package
        for package_manager, pkg_search_res in res.items():
            self.screen.pkg_group = res[pkg_mngr[0]]['group']
            self.pkg_group = res[pkg_mngr[0]]['group']
            if pkg_search_res['installed']:
                installed = True
                # if package emoji is still 📦, change it to the package manager emoji

        if installed:
            subtitle = f"[@click='screen.remove_package']🚮 [i]Remove[/i] {package}[/]"
        else:
            subtitle = f"[@click='screen.install_package']➕ [i]Install[/i] {package}[/]"

        # update package info
        self.screen.get_widget_by_id("pkg-info").border_title = (
                f"{emoji} [i]{package} info[/]"
                )
        note_box.border_subtitle = subtitle
        self.package = package
        self.screen.package = package

    def action_update_package_and_manager(self,
                                          package: str,
                                          package_manager: str) -> None:
        """
        update the package input box with a specific package
        """
        # updates the selection list
        pkg_mngrs_list = self.get_widget_by_id("pkg-mngr-list")
        pkg_mngrs_list.deselect_all()
        pkg_mngrs_list.select(
            pkg_mngrs_list.get_option(f"{package_manager[0]}-selection")
            )
        self.pkg_mngr = package_manager

        # updates the input box
        package_input_box = self.get_widget_by_id("package-name-input")
        package_input_box.clear()
        package_input_box.action_home()
        package_input_box.insert_text_at_cursor(package)

        # submit the package for searching
        self.search_for_package(package)
