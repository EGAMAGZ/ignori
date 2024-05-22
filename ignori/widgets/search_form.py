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
        & #ignore-container{
            & #ignore-list{
                width: 1fr;
            }
            & #ignore-code{
                width: 1fr !important;
            }
        }

        & #search-container{
            height: auto;

            & #search-input {
                width: 1fr;
            }

            & #search-button {
                width: auto;
            }
        }
    }
    """

    def compose(self: Self) -> ComposeResult:
        with Container():
            with Horizontal(id="search-container"):
                yield Input(placeholder="Search...", type="text", id="search-input")
                yield Button("Search", id="search-button")
            with Horizontal(id="ignore-container"):
                yield OptionList(
                    *[f"Option {position}" for position in range(20)],
                    id="ignore-list",
                )
                yield FilePreview("sample\ncode\nsampl\n" * 15, _id="ignore-code")
