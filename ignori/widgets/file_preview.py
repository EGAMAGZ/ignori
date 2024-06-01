from typing import Self

from rich.syntax import Syntax
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, VerticalScroll
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Static

from ignori.ignore_file import IgnoreFile


class FilePreview(
    Widget,
    can_focus=True,
    can_focus_children=False,
    inherit_bindings=False,
):

    DEFAULT_CSS = """
    FilePreview {
        height: auto;
        max-height: 100%;
        background: $boost;
        overflow-x: hidden;
        border: tall transparent;
        padding: 0 1;

        & #file-preview-label {
            width: 100%;
            background: $primary;
            color: $text;
            text-style: bold;
            padding: 0 1;
        }
    }

    FilePreview:focus {
        border: tall $accent;
    }
    """

    BINDINGS = [
        Binding("up", "scroll_up", "Scroll Up", show=False),
        Binding("down", "scroll_down", "Scroll Down", show=False),
        Binding("home", "scroll_home", "Scroll Home", show=False),
        Binding("end", "scroll_end", "Scroll End", show=False),
        Binding("pageup", "page_up", "Page Up", show=False),
        Binding("pagedown", "page_down", "Page Down", show=False),
    ]

    highlighted_ignore_file: reactive[IgnoreFile | None] = reactive(None)

    def action_scroll_up(self: Self) -> None:
        self.query_one(VerticalScroll).scroll_up()

    def action_scroll_down(self: Self) -> None:
        self.query_one(VerticalScroll).scroll_down()

    def action_scroll_home(self: Self) -> None:
        self.query_one(VerticalScroll).scroll_home()

    def action_scroll_end(self: Self) -> None:
        self.query_one(VerticalScroll).scroll_end()

    def action_page_up(self: Self) -> None:
        self.query_one(VerticalScroll).scroll_page_up()

    def action_page_down(self: Self) -> None:
        self.query_one(VerticalScroll).scroll_page_down()

    def watch_highlighted_ignore_file(
        self: Self,
        ignore_file: IgnoreFile | None,
    ) -> None:
        vertical_scroll = self.query_one(VerticalScroll)
        preview = self.query_one("#file-preview-code", expect_type=Static)

        preview.set_class(ignore_file is None, "muted-text")
        if ignore_file:
            vertical_scroll.scroll_home(animate=False)
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
        with Container(id="file-preview-container"):
            yield Label("Preview", id="file-preview-label")
            with VerticalScroll():
                yield Static(
                    id="file-preview-code",
                    expand=True,
                )
