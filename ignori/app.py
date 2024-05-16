import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, Input

from ignori.util.settings import APP_TITLE, STYLES_PATH


class IgnoriApp(App):
    TITLE = APP_TITLE
    CSS_PATH = str(STYLES_PATH / "global.tcss")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Search...")
        yield Label(os.getcwd())
        yield Footer()
