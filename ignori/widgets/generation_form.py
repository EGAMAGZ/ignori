from pathlib import Path
from typing import Self

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Button, Input


class GenerationForm(Widget):

    DEFAULT_CSS = """
    GenerationForm{
        & #path-container{
            & #path-input{
                width: 1fr;
            }

            & #path-button{
                width: auto;
            }
        }
    }
    """

    def __init__(self: "GenerationForm") -> None:
        super().__init__()
        self.log("ASD")

    @on(Button.Pressed, selector="#path-button")
    def generate_file(self: Self, event: Button.Pressed) -> None:
        path_input = self.query_one(selector="#path-input", expect_type=Input)
        path = Path(path_input.value)
        if not path.exists():
            self.notify("Path does not exist", severity="error")
            return

        if not path.is_dir():
            self.notify("Path is not a directory", severity="error")
            return

        self.notify(f"Path: {path}")

    def compose(self: Self) -> ComposeResult:
        with Horizontal(id="path-container"):
            yield Input(
                id="path-input",
                placeholder=f"{Path.cwd()}",
                type="text",
            )
            yield Button("Generate", id="path-button")
