from typing import Self

from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class InfoModal(ModalScreen[None]):
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
