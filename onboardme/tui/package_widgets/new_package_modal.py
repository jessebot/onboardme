# from onboardme.tui.validators.already_exists import CheckIfNameAlreadyInUse

from textual import on
from textual.binding import Binding
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.validation import Length
from textual.widgets import Button, Input, Label
from textual.suggester import SuggestFromList


class NewPackageModalScreen(ModalScreen):
    CSS_PATH = ["../css/base_modal.tcss",
                "../css/package_info.tcss"]
    BINDINGS = [Binding(key="b,escape,q",
                        key_display="b",
                        action="app.pop_screen",
                        description="Back")]


    def __init__(self,
                 package_manager_configs: dict,
                 package_manager: str,
                 package_group: str,
                 package: str) -> None:
        self.cfg = package_manager_configs
        self.pkg_mngr = package_manager
        self.pkg_group = package_group
        self.package = package
        super().__init__()

    def compose(self) -> ComposeResult:
        # base screen grid
        question = (
                f"Please confirm the group to [#ffaff9]install[/] [#C1FF87]{self.package}[/] into"
                )

        with Grid(id="new-package-modal-screen"):
            # grid for app question and buttons
            with Grid(id="question-box"):
                yield Label(question, id="modal-text")

                package_groups = []
                for package_mngr, metadata in self.cfg.items():
                    package_groups.extend(metadata['packages'].keys())

                print(package_groups)

                # grid for pckage manager dropdown and package input
                input = Input(validators=[Length(minimum=2)],
                              suggester=SuggestFromList(package_groups),
                              value=self.pkg_group,
                              placeholder="Name package group",
                              id="package-group-input")
                input.tooltip = "Name of the group to install package in" 
                yield input

                with Grid(id="modal-button-box"):
                    cancel = Button("🤷 cancel", id="cancel-button")
                    cancel.tooltip = "cancel search and install"
                    yield cancel

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

    @on(Input.Submitted)
    def input_submitted(self, event: Input.Submitted) -> None:
        """ 
        validate input on text submitted
        """
        description_grid = self.get_widget_by_id("description-buttons")
        print(f"event.value for input submitted is {event.value}")

        # create buttons based on which package manager found the package
        submit = Button(self.pkg_mngr, id="package-submit")
        submit.tooltip = f"install with {self.pkg_mngr}"
        description_grid.mount(submit)

    @on(Button.Pressed)
    def button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "package-submit":
            package_name = self.get_widget_by_id("package-name-input").value
            self.dismiss([package_name, self.pkg_mngr])
        else:
            self.dismiss([None, None, None])
