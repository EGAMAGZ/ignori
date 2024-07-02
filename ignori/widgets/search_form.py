from typing import Self

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Input, OptionList
from textual.widgets.option_list import Option

from ignori.ignore_file import IgnoreFile
from ignori.util.file import get_gitignore_templates
from ignori.widgets.file_preview import FilePreview
from ignori.widgets.language_list import LanguageList


def get_option_by_id(
    ignore_files: list[IgnoreFile],
    option_id: str,
) -> IgnoreFile | None:
    selected_file = next(
        (file for file in ignore_files if file.id == option_id),
        None,
    )
    return selected_file


class SearchForm(Widget):

    DEFAULT_CSS = """
    SearchForm {
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

    class Selected(Message):
        def __init__(
            self: "SearchForm.Selected",
            selected_file: IgnoreFile | None,
        ) -> None:
            self.selected_file = selected_file
            super().__init__()

    ignore_files: reactive[list[IgnoreFile]] = reactive(get_gitignore_templates())
    filtered_ignore_files: reactive[list[IgnoreFile]] = reactive([])
    search_name: reactive[str] = reactive("")

    highlighted_ignore_file: reactive[IgnoreFile | None] = reactive(None)

    @on(Button.Pressed, selector="#search-button")
    def search_ignore_file(self: Self, event: Button.Pressed) -> None:
        path_input = self.query_one(selector="#search-input", expect_type=Input)

        self.search_name = path_input.value

    @on(OptionList.OptionHighlighted, selector="#ignore-list")
    def show_file_content(self: Self, event: OptionList.OptionHighlighted) -> None:
        if event.option_id:
            highligted_file = get_option_by_id(self.ignore_files, event.option_id)

            if highligted_file:
                self.highlighted_ignore_file = highligted_file

    @on(OptionList.OptionSelected, selector="#ignore-list")
    def select_file(self: Self, event: OptionList.OptionSelected) -> None:
        if event.option_id:
            selected_file = get_option_by_id(self.ignore_files, event.option_id)

            if selected_file:
                self.post_message(self.Selected(selected_file))
                self.notify(f"{selected_file.language} selected", title="Success")

    def compute_filtered_ignore_files(self: Self) -> list[IgnoreFile]:
        return [
            file for file in self.ignore_files
            if self.search_name.lower() in file.language.lower()
        ]

    def watch_filtered_ignore_files(self: Self, ignore_files: list[IgnoreFile]) -> None:
        ignore_list = self.query_one("#ignore-list", expect_type=OptionList)
        ignore_list.clear_options()

        if ignore_files:
            ignore_list.add_options(
                [Option(file, id=file.id) for file in ignore_files],
            )
        else:
            ignore_list.add_option(Option("No files found", disabled=True))

    def compose(self: Self) -> ComposeResult:
        with Container():
            with Horizontal(id="search-container"):
                yield Input(placeholder="Search...", type="text", id="search-input")
                yield Button("Search", id="search-button")
            with Horizontal(id="ignore-container"):
                yield LanguageList(id="ignore-list")
                yield FilePreview(id="ignore-code").data_bind(
                    SearchForm.highlighted_ignore_file,
                )
