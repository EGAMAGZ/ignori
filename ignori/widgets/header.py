from typing import Self

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Label

from ignori.util.settings import APP_TITLE, APP_VERSION


class Header(Horizontal):
    def compose(self: Self) -> ComposeResult:
        yield Label(APP_TITLE, id="app-title")
        yield Label(f"v{APP_VERSION}", id="app-version")
