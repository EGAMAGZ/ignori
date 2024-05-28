from pathlib import Path
from typing import Self

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Input, Label

from ignori.ignore_file import IgnoreFile
from ignori.util.file import copy_file_content
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

    class Generated(Message):
        def __init__(self: "GenerationForm.Generated") -> None:
            self.selected_file = None
            super().__init__()

    selected_ignore_file: reactive[IgnoreFile | None] = reactive(None)

    def watch_selected_ignore_file(self: Self, ignore_file: IgnoreFile | None) -> None:
        label = self.query_one("#path-label", expect_type=Label)
        label.update(
            (
                f"Language: {ignore_file.language}"
                if ignore_file
                else "No language selected"
            ),
        )

    @on(Button.Pressed, selector="#path-button")
    def generate_file(self: Self) -> None:
        input_field = self.query_one("#path-input", expect_type=Input)
        result = input_field.validate(input_field.value)
        if not input_field.is_valid and result:
            self.notify(
                "".join(result.failure_descriptions),
                title="Error",
                severity="error",
            )
            return

        if self.selected_ignore_file is None:
            self.notify("No language selected", title="Error", severity="error")
            return

        copy_file_content(
            source_file=self.selected_ignore_file.path,
            destination_path=Path(input_field.value),
        )

        self.notify("File generated successfully", title="Success")
        self.reset_form()

    def reset_form(self: Self) -> None:
        self.query_one(selector="#path-input", expect_type=Input).clear()
        self.post_message(self.Generated())

    def compose(self: Self) -> ComposeResult:
        with Container(id="path-container"):
            yield Label(
                "No language selected",
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
