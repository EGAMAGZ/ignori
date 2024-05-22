from typing import Self

from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widget import Widget
from textual.widgets import Button, Input, OptionList

from ignori.widgets.file_preview import FilePreview


class SearchForm(Widget):

    DEFAULT_CSS = """
    SearchForm{
        width: 100%;

        & OptionList{
            width: 1fr;
        }
        & FilePreview{
            width: 1fr !important;
        }

        & #search-container{
            height: auto;

            & Input{
                width: 1fr;
            }

            & Button{
                width: auto;
            }
        }
    }
    """

    def compose(self: Self) -> ComposeResult:
        with Container():
            with Horizontal(id="search-container"):
                yield Input(placeholder="Search...", type="text")
                yield Button("Search")
            with Horizontal():
                yield OptionList(*[f"Option {position}" for position in range(20)])
                yield FilePreview("sample\ncode\nsampl\n" * 15)
