from typing import Self

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Label

from ignori.util.settings import APP_TITLE, APP_VERSION


class Header(Horizontal):

    DEFAULT_CSS = """\
    Header {
        background: $primary;
        height: 1;
        margin-bottom: 1;
        padding: 0 2;

        & #app-title {
            width: 1fr;
            content-align: center middle;
        }

        & #app-version {
            content-align: left middle;
            color: $text 40%;
            text-style: italic;
        }
    }
    """

    def compose(self: Self) -> ComposeResult:
        yield Label(APP_TITLE, id="app-title")
        yield Label(APP_VERSION, id="app-version")
