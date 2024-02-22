# from onboardme.tui.validators.already_exists import CheckIfNameAlreadyInUse
from onboardme.packages.search import search_for_package

from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.validation import Length
from textual.widgets import Button, Input, Label, Select
from textual.widget import Widget


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
        input = Input(validators=[Length(minimum=2)],
                      placeholder="Name of your package",
                      id="package-name-input")
        input.tooltip = "Name for your package in onboardme"

        # grid for pckage manager dropdown and package input
        with Grid(id="package-search-inputs"):
            yield Select.from_values(self.cfg.keys(),
                                     value=self.pkg_mngr,
                                     prompt="All Package Managers",
                                     allow_blank=True,
                                     classes="select-dropdown")
            yield input

        # response from package search
        yield Label("", id="package-res")

    @on(Input.Changed)
    def input_validation(self, event: Input.Changed) -> None:
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

    @on(Select.Changed)
    def dropdown_selected(self, event: Select.Changed) -> None:
        """ 
        change the default package manager based on dropdown option selected
        """
        if event.value:
            self.pkg_mngr = event.value
        else:
            self.pkg_mngr = self.cfg.keys()

    @on(Input.Submitted)
    def input_submitted(self, event: Input.Submitted) -> None:
        """ 
        validate input on text submitted and update res Label
        """
        print(f"event.value for input submitted is {event.value}")
        res = search_for_package(
                package=event.value,
                package_manager=self.pkg_mngr,
                cfg=self.cfg
                )

        # create buttons based on which package manager found the package
        if isinstance(res, str):
            submit = Button(self.pkg_mngr, id="package-submit")
            submit.tooltip = f"install with {self.pkg_mngr}"
            formatted_res = res.replace('\n','\n\n')
        elif isinstance(res, list):
            joined_res = "\n".join(res)
            formatted_res = joined_res.replace('\n','\n\n')

        res_label = self.get_widget_by_id("package-res")
        res_label.update(formatted_res)
