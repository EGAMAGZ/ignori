from typing import Self

from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class InfoModal(ModalScreen):

    DEFAULT_CSS = """
    InfoModal {
        align: center middle;
    }

    InfoModal > Container {
        width: auto;
        height: auto;
        border: tall $secondary 80%;
        background: $surface;
        padding: 2 4;
    }

    InfoModal > Container > Label {
        width: 100%;
        content-align-horizontal: center;
        margin-top: 1;
    }

    InfoModal > Container > Button {
        margin: 2 4;
        width: auto;
        height: auto;
    }
    """

    message: str
    button_text: str

    def __init__(self: "InfoModal", message: str, button_text: str = "Ok") -> None:
        super().__init__()
        self.message = message
        self.button_text = button_text

    def compose(self: Self) -> ComposeResult:
        with Container():
            yield Label(self.message)
            yield Button(self.button_text, variant="primary", id="close-button")

    @on(Button.Pressed, "#close-button")
    def close_modal(self: Self, event: Button.Pressed) -> None:
        self.app.pop_screen()
