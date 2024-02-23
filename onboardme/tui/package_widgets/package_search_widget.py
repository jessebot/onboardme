# from onboardme.tui.validators.already_exists import CheckIfNameAlreadyInUse
from onboardme.packages.search import search_for_package

from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.events import Mount
from textual.validation import Length
from textual.widget import Widget
from textual.widgets import Button, Input, Label, SelectionList
from textual.widgets.selection_list import Selection


class PackageSearch(Widget):
    """ 
    widget to search for packages for one or more package managers
    """
    CSS_PATH = ["../css/base_modal.tcss",
                "../css/package_info.tcss"]

    def __init__(self,
                 package_manager_configs: dict = {},
                 package_manager: str|list = None,
                 id: str = None) -> None:
        self.cfg = package_manager_configs
        if not package_manager:
            self.pkg_mngr = None
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
            if self.pkg_mngr == pkg_mgr:
                selection_dict["initial_state"] = True

            selections.append(Selection(**selection_dict))

        selection_list = SelectionList[str](*selections, id="pkg-mngr-list")
        selection_list.tooltip = "Package Managers to search"

        # create input for package to search for
        input = Input(validators=[Length(minimum=2)],
                      placeholder="Name of your package",
                      id="package-name-input")
        input.tooltip = "Name for your package in onboardme"


        # grid for pckage manager selection list and package search input
        with Grid(id="package-search-inputs"):
            yield selection_list
            yield input

        # response from package search
        yield Label("[i]Search[/] for a package for more info.",
                    id="package-res")

    def on_mount(self) -> None:
        """
        tidy the borders
        """
        self.get_widget_by_id("package-res").border_title = "📦 [i]Package Info[/i]"

    @on(Input.Submitted)
    def input_validation(self, event: Input.Submitted) -> None:
        """ 
        validate input on any text entered
        """
        if event.input.id == "package-name-input":
            if not event.validation_result.is_valid:
                # if result is not valid, notify the user why
                self.notify("\n".join(event.validation_result.failure_descriptions),
                            severity="warning",
                            title="⚠️ Input Validation Error\n")
                self.app.bell()

    @on(Mount)
    @on(SelectionList.SelectedChanged)
    def update_selected_view(self) -> None:
        self.pkg_mngr = self.get_widget_by_id("pkg-mngr-list").selected

    @on(Input.Submitted)
    def input_submitted(self, event: Input.Submitted) -> None:
        """ 
        validate input on text submitted and update res Label
        """
        self.search_for_package(event.value)

    def search_for_package(self, package: str) -> None:
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

        if isinstance(res, str):
            # create buttons based on which package manager found the package
            submit = Button(pkg_mngr, id="package-submit")
            submit.tooltip = f"install with {pkg_mngr}"
            formatted_res = res.replace('\n','\n\n').lstrip()

        # for a result for a single package manager that includes multiple packages
        elif isinstance(res, list):
            joined_res = "\n".join(res)
            formatted_res = joined_res.replace('\n','\n\n')

        # for multiple package manger results
        elif isinstance(res, dict):
            formatted_res = ""

            for package_manager, pkg_search_res in res.items():

                # if the result for a package manger search includes multiple packages
                if isinstance(pkg_search_res, list):
                    joined_res = "\n".join(pkg_search_res)
                    formatted_res += f"{package_manager}:\n{pkg_search_res}"

        elif not res:
            formatted_res = "no result :("

        res_label = self.get_widget_by_id("package-res")
        res_label.update(formatted_res)

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
            pkg_mngrs_list.get_option(f"{package_manager}-selection")
            )
        self.pkg_mngr = package_manager

        # updates the input box
        package_input_box = self.get_widget_by_id("package-name-input")
        package_input_box.clear()
        package_input_box.action_home()
        package_input_box.insert_text_at_cursor(package)

        # submit the package for searching
        self.search_for_package(package)
