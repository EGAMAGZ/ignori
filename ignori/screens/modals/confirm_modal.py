from typing import Self

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class ConfirmModal(ModalScreen[bool]):
    message: str

    def __init__(self: "ConfirmModal", *, message: str) -> None:
        super().__init__()
        self.message = message

    @on(Button.Pressed)
    def close_model(self: Self, event: Button.Pressed) -> None:
        self.dismiss(event.control.id == "yes")

    def compose(self: Self) -> ComposeResult:
        with Container():
            yield Label(self.message)
            with Horizontal():
                yield Button("Yes", id="yes", variant="success")
                yield Button("No", id="no", variant="error")
