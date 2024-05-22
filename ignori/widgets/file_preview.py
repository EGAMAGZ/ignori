from typing import Self

from rich.syntax import Syntax
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widget import Widget
from textual.widgets import Label, Static


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

    def __init__(self: "FilePreview", code: str) -> None:
        super().__init__()
        self.code = code

    def on_mount(self: Self) -> None:
        # TODO: Change for Syntaz.from_path()
        self.query_one("#preview", expect_type=Static).update(
            Syntax(self.code, "plain", line_numbers=True, word_wrap=False),
        )

    def compose(self: Self) -> ComposeResult:
        with Container():
            yield Label("Preview", id="file-name")
            with VerticalScroll():
                yield Static(
                    id="preview",
                    expand=True,
                )
