from functools import partial
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
from ignori.screens.modals.confirm_modal import ConfirmModal
from ignori.util.file import copy_file_content
from ignori.util.settings import DEFAULT_OUTPUT_FILE
from ignori.util.validators import PathValidator
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
        &.-activate {
            border: none;
        }
    }"""


class GenerationForm(Widget):
    class Generated(Message):
        """Event sent when `.gitignore` file is generated"""

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

        self.validate_generation(
            source_file=self.selected_ignore_file.path,
            output_path=Path(input_field.value),
        )

    def validate_generation(self: Self, source_file: Path, output_path: Path) -> None:
        def handle_confirm(
            response: bool | None,
            source_file: Path,
            output_file: Path,
        ) -> None:
            if response:
                copy_file_content(
                    source_file=source_file,
                    output_file=output_file,
                )
                self.notify("File generated successfully", title="Success")
                self.reset_form()

        output_file = output_path / DEFAULT_OUTPUT_FILE
        if output_file.exists():
            confirm_callback = partial(
                handle_confirm,
                source_file=source_file,
                output_file=output_file,
            )
            self.app.push_screen(
                screen=ConfirmModal(
                    message=".gitignore already exists. Do you want to overwrite it?",
                ),
                callback=confirm_callback,
            )
        else:
            copy_file_content(
                source_file=source_file,
                output_file=output_file,
            )
            self.notify("File generated successfully", title="Success")
            self.reset_form()

    def reset_form(self: Self) -> None:
        self.query_one(selector="#path-input", expect_type=Input).clear()
        self.post_message(self.Generated())

    def compose(self: Self) -> ComposeResult:
        with Horizontal():
            yield Label("Language:", classes="label")
            yield LanguageBadge(id="language-badge").data_bind(
                language_selected=GenerationForm.selected_ignore_file,
            )
        with Horizontal(id="path-form-container"):
            yield Label("Output:", classes="label")
            yield Input(
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
