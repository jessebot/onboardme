# from onboardme.tui.validators.already_exists import CheckIfNameAlreadyInUse
from onboardme.packages.search import search_for_package

from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.validation import Length
from textual.widgets import Button, Input, Label, Select, Pretty
from textual.widget import Widget


class PackageSearch(Widget):
    CSS_PATH = ["../css/base_modal.tcss",
                "../css/new_package_modal.tcss"]

    def __init__(self,
                 package_manager_configs: dict = {},
                 package_manager: str|list = None) -> None:
        self.cfg = package_manager_configs
        if not package_manager:
            self.pkg_mngr = None
        else:
            self.pkg_mngr = package_manager
        super().__init__()

    def compose(self) -> ComposeResult:
        # base screen grid
        # grid for app question and buttons
        with Grid(id="question-box"):
            # grid for pckage manager dropdown and package input
            input = Input(validators=[Length(minimum=2)],
                          placeholder="Name of your package",
                          id="package-name-input")
            input.tooltip = "Name for your package in onboardme"
            with Grid(id="package-search-inputs"):
                yield Select.from_values(self.cfg.keys(),
                                         value=self.pkg_mngr,
                                         prompt="All Package Managers",
                                         allow_blank=True,
                                         classes="select-dropdown")
                yield input

            desc_input = Grid(id="description-buttons")
            desc_input.tooltip = "To be displayed in the UI"
            yield desc_input

    def on_mount(self) -> None:
        box = self.get_widget_by_id("question-box")
        box.border_subtitle = "[@click=app.pop_screen]cancel[/]"

        if self.app.speak_screen_titles:
            # if text to speech is on, read screen title
            self.app.action_say(
                    "Screen title: Please enter a name for your package. "
                    "You can press escape to close this modal screen"
                    )

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
        change the default package manager
        """
        if event.value:
            self.pkg_mngr = event.value
        else:
            self.pkg_mngr = self.cfg.keys()

    @on(Input.Submitted)
    def input_submitted(self, event: Input.Submitted) -> None:
        """ 
        validate input on text submitted
        """
        description_grid = self.get_widget_by_id("description-buttons")
        print(f"event.value for input submitted is {event.value}")
        res = search_for_package(
                package=event.value,
                package_manager=self.pkg_mngr,
                cfg=self.cfg
                )

        # create buttons based on which package manager found the package
        if isinstance(self.pkg_mngr, str):
            submit = Button(self.pkg_mngr, id="package-submit")
            submit.tooltip = f"install with {self.pkg_mngr}"
            description_grid.mount(Label(res.replace('\n','\n\n')))
        else:
            description_grid.mount(Pretty(res))
