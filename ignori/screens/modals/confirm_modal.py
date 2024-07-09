from typing import Self

from textual.app import ComposeResult, on
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class ConfirmModal(ModalScreen[bool]):
    DEFAULT_CSS = """\
    ConfirmModal {
        align: center middle;
    }

    ConfirmModal > Container {
        width: auto;
        height: auto;
        border: thick $background 80%;
        background: $surface;
    }

    ConfirmModal > Container > Label {
        width: 100%;
        content-align-horizontal: center;
        margin-top: 1;
    }

    ConfirmModal > Container > Horizontal {
        width: auto;
        height: auto;
    }

    ConfirmModal > Container > Horizontal > Button {
        margin: 2 4;
    }"""

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
                yield Button("No", id="no", variant="error")
                yield Button("Yes", id="yes", variant="success")
