from typing import Self

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, OptionList

from ignori.util.settings import APP_TITLE, STYLES_PATH
from ignori.widgets.file_preview import FilePreview
from ignori.widgets.generation_form import GenerationForm


class IgnoriApp(App):
    TITLE = APP_TITLE
    CSS_PATH = str(STYLES_PATH / "global.tcss")

    BINDINGS = [Binding(key="d", action="toggle_dark", description="Toggle Dark Mode")]

    def compose(self: Self) -> ComposeResult:
        yield Header()
        with Vertical():
            with Container():
                with Horizontal(id="search-container"):
                    yield Input(placeholder="Search...", type="text")
                    yield Button("Search")
                with Horizontal():
                    yield OptionList(*[f"Option {position}" for position in range(20)])
                    yield FilePreview("sample\ncode\nsampl\n" * 15)

            yield GenerationForm()
        yield Footer()
