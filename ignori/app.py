from typing import Self

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import Footer, Header

from ignori.ignore_file import IgnoreFile
from ignori.util.settings import APP_TITLE, STYLES_PATH
from ignori.widgets.generation_form import GenerationForm
from ignori.widgets.search_form import SearchForm


class IgnoriApp(App):
    TITLE = APP_TITLE
    CSS_PATH = str(STYLES_PATH / "global.tcss")

    BINDINGS = [
        Binding(key="d", action="toggle_dark", description="Toggle Dark Mode"),
    ]

    selected_ignore_file: reactive[IgnoreFile | None] = reactive(None)

    @on(SearchForm.Selected)
    def selected_file(self: Self, event: SearchForm.Selected) -> None:
        self.selected_ignore_file = event.selected_file

    def compose(self: Self) -> ComposeResult:
        yield Header()
        with Vertical(id="container"):
            yield SearchForm()
            yield GenerationForm().data_bind(IgnoriApp.selected_ignore_file)
        yield Footer()
