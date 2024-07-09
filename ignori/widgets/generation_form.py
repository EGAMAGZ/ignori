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
from ignori.widgets.input import BorderlessInput
from ignori.widgets.language_badge import LanguageBadge


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
            & Label {
                padding: 0 1;
                background: $primary-darken-3;
            }
        }
    }
    """

    class Generated(Message): ...

    selected_ignore_file: reactive[IgnoreFile | None] = reactive(None)

    @on(Button.Pressed, selector="#path-button")
    @on(Input.Submitted, selector="#path-input")
    def generate_file(self: Self, event: Input.Submitted | Button.Pressed) -> None:
        if isinstance(event, Input.Submitted):
            input_field = event.control
            result = event.validation_result
        elif isinstance(event, Button.Pressed):
            input_field = self.query_one("#path-input", expect_type=Input)
            result = input_field.validate(input_field.value)

        if not input_field.is_valid and result:
            self.notify(
                "".join(result.failure_descriptions),
                title="Error",
                severity="error",
            )
            input_field.focus()
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
        yield LanguageBadge().data_bind(
            language_selected=GenerationForm.selected_ignore_file,
        )
        with Horizontal(id="path-form-container"):
            yield Label("Output:")
            yield BorderlessInput(
                id="path-input",
                placeholder=f"{Path.cwd()}",
                type="text",
                validators=[
                    PathValidator(),
                ],
                validate_on=[
                    "blur",
                    "submitted",
                ],
            )
            yield PathGenerationButton(
                "Generate",
                id="path-button",
            )
