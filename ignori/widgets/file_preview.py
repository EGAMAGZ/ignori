from typing import Self

from rich.syntax import Syntax
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Static

from ignori.ignore_file import IgnoreFile


class FilePreview(Widget):

    DEFAULT_CSS = """
    FilePreview{
        width: auto;

        & #file-name {
            width: 100%;
            background: $primary;
            color: $text;
        }
    }
    """

    highlighted_ignore_file: reactive[IgnoreFile | None] = reactive(None)

    def __init__(self: "FilePreview", _id: str) -> None:
        super().__init__(id=_id)

    def watch_highlighted_ignore_file(
        self: Self,
        ignore_file: IgnoreFile | None,
    ) -> None:
        if ignore_file is not None:
            self.query_one(VerticalScroll).scroll_home(animate=False)
            self.query_one("#preview", expect_type=Static).update(
                Syntax.from_path(
                    str(ignore_file.path),
                    line_numbers=True,
                    word_wrap=True,
                ),
            )

    def compose(self: Self) -> ComposeResult:
        with Container():
            yield Label("Preview", id="file-name")
            with VerticalScroll():
                yield Static(
                    id="preview",
                    expand=True,
                )
