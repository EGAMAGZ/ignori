from typing import Self

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import Footer

from ignori.ignore_file import IgnoreFile
from ignori.util.settings import APP_TITLE, STYLES
from ignori.widgets.generation_form import GenerationForm
from ignori.widgets.header import Header
from ignori.widgets.language_badge import LanguageBadge
from ignori.widgets.search_form import SearchForm


class IgnoriApp(App[None], inherit_bindings=False):
    TITLE = APP_TITLE
    CSS_PATH = STYLES  # type: ignore

    BINDINGS = [
        Binding(
            key="ctrl+q",
            action="quit",
            description="Quit",
            priority=True,
        ),
    ]

    selected_ignore_file: reactive[IgnoreFile | None] = reactive(None)

    @on(LanguageBadge.Pressed)
    def unselect_file(self: Self, event: LanguageBadge.Pressed) -> None:
        self.selected_ignore_file = None

    @on(SearchForm.Selected)
    def selected_file(self: Self, event: SearchForm.Selected) -> None:
        self.selected_ignore_file = event.selected_file

    @on(GenerationForm.Generated)
    def generated_file(self: Self, event: GenerationForm.Generated) -> None:
        self.selected_ignore_file = None

    def compose(self: Self) -> ComposeResult:
        yield Header()
        with Vertical(id="container"):
            yield SearchForm()
            yield GenerationForm().data_bind(IgnoriApp.selected_ignore_file)
        yield Footer()


def main() -> None:
    app = IgnoriApp()
    app.run()


if __name__ == "__main__":
    main()
