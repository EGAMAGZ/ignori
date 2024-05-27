from pathlib import Path
from typing import Self

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Input, Label

from ignori.ignore_file import IgnoreFile
from ignori.util.validators import PathValidator


class GenerationForm(Widget):

    DEFAULT_CSS = """
    GenerationForm {
        & #path-container {
            height: auto;
        }

        & #path-form-container{
            height: auto;
            & #path-input{
                width: 1fr;
            }

            & #path-button{
                width: auto;
            }
        }
    }
    """

    selected_ignore_file: reactive[IgnoreFile | None] = reactive(None)

    def watch_selected_ignore_file(self: Self, ignore_file: IgnoreFile | None) -> None:
        if ignore_file:
            label = self.query_one("#path-label", expect_type=Label)
            label.update("Language: " + ignore_file.language)

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
        with Container(id="path-container"):
            yield Label(
                "Path",
                id="path-label",
            )
            with Horizontal(id="path-form-container"):
                yield Input(
                    id="path-input",
                    placeholder=f"{Path.cwd()}",
                    type="text",
                    validators=[
                        PathValidator(),
                    ],
                )
                yield Button("Generate", id="path-button")
