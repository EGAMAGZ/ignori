from pathlib import Path
from typing import Self

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Input, Label

from ignori.ignore_file import IgnoreFile
from ignori.util.file import copy_file_content
from ignori.util.validators import PathValidator


class PathInput(Input):

    DEFAULT_CSS = """\
    PathInput {
        border: none;
        width: 1fr;
        height: 1;

        &:focus {
            /* TODO: CHECK WHY IS REQUIRED THE IMPORTANT */
            border: none !important;
            width: 1fr;
            height: 1 !important;

            & .input--cursor {
                color: $text;
                background: $accent-lighten-2;
            }
        }
    }
    """

class PathGenerationButton(Button):

    DEFAULT_CSS = """\
    PathGenerationButton {
        padding: 0 1;
        height: 1;
        min-width: 5;
        background: $primary;
        color: $text;
        border: none;
        text-style: none;

        &:hover {
            text-style: b;
            padding: 0 1;
            border: none;
            background: $primary-darken-1;
        }
    }
    """

class GenerationForm(Widget):

    DEFAULT_CSS = """\
    GenerationForm {
        padding: 1;
        & #path-form-container{
            height: 1;
        }
    }
    """

    class Generated(Message):
        ...

    selected_ignore_file: reactive[IgnoreFile | None] = reactive(None)

    def watch_selected_ignore_file(self: Self, ignore_file: IgnoreFile | None) -> None:
        label = self.query_one("#path-label", expect_type=Label)
        label.update(
            (
                f"[b]Language:[/b] {ignore_file.language}"
                if ignore_file
                else "No language selected"
            ),
        )

        label.set_class(ignore_file is None, "muted-text")
        label.set_class(ignore_file is not None, "highlighted-text")

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
        yield Label(
            "No language selected",
            id="path-label",
        )
        with Horizontal(id="path-form-container"):
            yield PathInput(
                id="path-input",
                placeholder=f"{Path.cwd()}",
                type="text",
                validators=[
                    PathValidator(),
                ],
            )
            yield PathGenerationButton(
                    "Generate",
                    id="path-button",
            )
