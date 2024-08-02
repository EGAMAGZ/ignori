from typing import Self

from rich.syntax import Syntax
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widgets import Static

from ignori.ignore_file import IgnoreFile


class FilePreview(
    VerticalScroll,
    can_focus=True,
    can_focus_children=False,
):
    BORDER_TITLE = "Preview"

    highlighted_ignore_file: reactive[IgnoreFile | None] = reactive(None)

    def watch_highlighted_ignore_file(
        self: Self,
        ignore_file: IgnoreFile | None,
    ) -> None:
        preview = self.query_one("#file-preview-code", expect_type=Static)

        preview.set_class(ignore_file is None, "muted-text")
        if ignore_file:
            self.scroll_home(animate=False)
            preview.update(
                Syntax.from_path(
                    str(ignore_file.path),
                    line_numbers=True,
                    word_wrap=True,
                    theme="github-dark",
                ),
            )
        else:
            preview.update("No file selected")

    def compose(self: Self) -> ComposeResult:
        yield Static(
            id="file-preview-code",
            expand=True,
        )
