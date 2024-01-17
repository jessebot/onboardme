#!/usr/bin/env python3.11
# internal library
from onboardme.tui.validators.already_exists import CheckIfNameAlreadyInUse

# external libraries
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Horizontal
from textual.screen import ModalScreen
from textual.suggester import SuggestFromList
from textual.validation import Length
from textual.widgets import Input, Button, Label, Switch


PACKAGE_MANAGER_SUGGESTIONS = SuggestFromList((
       "appimage",
       "apt",
       "brew",
       "flatpak",
       "pip",
       "snap"
       ))


def placeholder_grammar(key: str) -> str:
    """
    generates a grammatically correct placeolder string for inputs
    """
    article = ""

    # check if this is a plural (ending in s) and if ip address pool
    plural = key.endswith('s') or key == "address_pool"
    if plural:
        plural = True

    # check if the key starts with a vowel
    starts_with_vowel = key.startswith(('o','a','e'))

    # create a gramatically corrrect placeholder
    if starts_with_vowel and not plural:
        article = "an"
    elif not starts_with_vowel and not plural:
        article = "a"

    # if this is plural change the grammar accordingly
    if plural:
        return f"Enter a comma seperated list of {key}"
    else:
        return f"Enter {article} {key}"


def create_sanitized_list(input_value: str) -> list:
    """
    take string and split by , or ' ' if there are any in it. returns list of
    items if no comma or space in string, returns list with string as only index
    """

    # split by comma, thereby generating a list from a csv
    if "," in input_value:
        input_value = input_value.replace(" ","")
        value = input_value.split(",")

    # split by spaces, thereby generating a list from a space delimited list
    elif "," not in input_value and " " in input_value:
        value = input_value.split(" ")

    # otherwise just use the value
    else:
        value = [input_value]

    return value


def format_description(description: str = ""):
    """
    change description to dimmed colors
    links are changed to steel_blue and not dimmed
    """
    if not description:
        description = "No Description provided yet for this user defined application."

    description = description.replace("[link", "[steel_blue][link")
    description = description.replace("[/link]", "[/link][/steel_blue]")

    return f"""{description}"""


def bool_option(label: str, switch_value: bool, name: str, tooltip: str) -> Horizontal:
    """
    returns a label and switch row in a Horizontal container
    """
    bool_label = Label(label, classes="bool-switch-row-label")
    bool_label.tooltip = tooltip

    switch = Switch(value=switch_value,
                    classes="bool-switch-row-switch",
                    name=name,
                    id=label)
    switch.tooltip = tooltip

    extra_class = name.replace('_',"-")
    return Horizontal(bool_label, switch, classes=f"bool-switch-row {extra_class}")


def input_field(label: str, initial_value: str, name: str, placeholder: str,
                tooltip: str = "") -> Horizontal:
    """
    returns an input label and field within a Horizontal container
    """
    input_label = Label(label, classes="input-row-label")
    input_label.tooltip = tooltip

    input_dict = {"placeholder": placeholder,
                  "classes": "input-row-input",
                  "id": label,
                  "name": name}
    if initial_value:
        input_dict["value"] = initial_value
    else:
        input_dict["value"] = ""

    input = Input(**input_dict)
    input.tooltip = tooltip

    return Horizontal(input_label, input, classes="input-row")
