from typing import Self

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Input, OptionList

from ignori.ignore_file import IgnoreFile
from ignori.util.file import search_files_by_name
from ignori.widgets.file_preview import FilePreview


class SearchForm(Widget):

    DEFAULT_CSS = """
    SearchForm{
        width: 100%;
        & #ignore-container{
            & OptionList {
                width: 1fr;
                height:100%;
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

    ignore_files: reactive[list[IgnoreFile]] = reactive(search_files_by_name())

    @on(Button.Pressed, selector="#search-button")
    def search_ignore_file(self: Self, event: Button.Pressed) -> None:
        path_input = self.query_one(selector="#search-input", expect_type=Input)

        self.ignore_files = search_files_by_name(path_input.value)

    def watch_ignore_files(self: Self, ignore_files: list[IgnoreFile]) -> None:
        ignore_list = self.query_one("#ignore-list", expect_type=OptionList)
        ignore_list.clear_options()

        ignore_list.add_options([file.language for file in ignore_files])

    def compose(self: Self) -> ComposeResult:
        with Container():
            with Horizontal(id="search-container"):
                yield Input(placeholder="Search...", type="text", id="search-input")
                yield Button("Search", id="search-button")
            with Horizontal(id="ignore-container"):
                yield OptionList(
                    id="ignore-list",
                )
                yield FilePreview("sample\ncode\nsampl\n" * 15, _id="ignore-code")
