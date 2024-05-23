from typing import Self

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Input, OptionList
from textual.widgets.option_list import Option

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

    selected_ignore_file: reactive[IgnoreFile | None] = reactive(None)

    @on(Button.Pressed, selector="#search-button")
    def search_ignore_file(self: Self, event: Button.Pressed) -> None:
        path_input = self.query_one(selector="#search-input", expect_type=Input)

        self.ignore_files = search_files_by_name(path_input.value)

    @on(OptionList.OptionHighlighted, selector="#ignore-list")
    def show_file_content(self: Self, event: OptionList.OptionHighlighted) -> None:
        pass

    @on(OptionList.OptionSelected, selector="#ignore-list")
    def select_file(self: Self, event: OptionList.OptionSelected) -> None:
        if event.option_id is not None:
            ignore_file = list(
                filter(lambda file: file.id == event.option_id, self.ignore_files),
            )[0]
            self.selected_ignore_file = ignore_file
            self.notify(ignore_file.language)

    def watch_ignore_files(self: Self, ignore_files: list[IgnoreFile]) -> None:
        ignore_list = self.query_one("#ignore-list", expect_type=OptionList)
        ignore_list.clear_options()

        if ignore_files:
            ignore_list.add_options(
                [Option(file.language, id=file.id) for file in ignore_files],
            )
        else:
            ignore_list.add_option(Option("No files found", disabled=True))

    def compose(self: Self) -> ComposeResult:
        with Container():
            with Horizontal(id="search-container"):
                yield Input(placeholder="Search...", type="text", id="search-input")
                yield Button("Search", id="search-button")
            with Horizontal(id="ignore-container"):
                yield OptionList(
                    id="ignore-list",
                )
                yield FilePreview(_id="ignore-code").data_bind(
                    SearchForm.selected_ignore_file,
                )
