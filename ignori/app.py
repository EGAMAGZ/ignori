from pathlib import Path
from typing import Self

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input
from textual.containers import Horizontal
from textual.binding import Binding

from ignori.util.settings import APP_TITLE, STYLES_PATH


class IgnoriApp(App):
    TITLE = APP_TITLE
    CSS_PATH = str(STYLES_PATH / "global.tcss")

    BINDINGS = [Binding(key="d", action="toggle_dark", description="Toggle Dark Mode")]

    @on(Button.Pressed, selector="#path-button")
    def generate_file(self: Self, event: Button.Pressed) -> None:
        path_input = self.query_one(selector="#path-input", expect_type=Input)
        path = Path(path_input.value)
        if not path.exists():
            self.notify("Path does not exist", severity="error")
            return
        if not path.is_dir():
            self.notify("Path is not a directory", severity="error")
            return

        self.notify(f"Path: {path}")

    def compose(self: Self) -> ComposeResult:
        yield Header()
        with Horizontal(id="path-container"):
            yield Input(
                id="path-input",
                placeholder=f"{Path.cwd()}",
                type="text",
            )
            yield Button("Generate", id="path-button")
        yield Footer()
