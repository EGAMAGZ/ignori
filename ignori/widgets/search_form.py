from dataclasses import dataclass
from typing import Self

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Button, Input, OptionList
from textual.widgets.option_list import Option

from ignori.ignore_file import IgnoreFile, get_option_by_id
from ignori.util.file import get_gitignore_templates
from ignori.widgets.file_preview import FilePreview
from ignori.widgets.language_list import LanguageList


class SearchButton(Button):
    DEFAULT_CSS = """\
    SearchButton {
        height: 1;
        min-width: 5;
        background: $secondary;
        color: $text;
        border: none;
        text-style: none;

        &:hover {
            text-style: b;
            border: none;
            background: $secondary-darken-1;
        }
        &.-active {
            border: none;
        }
    }
    """


class SearchForm(Container):
    @dataclass
    class Selected(Message):
        """Event sent when language is selected"""

        selected_file: IgnoreFile | None

    ignore_files: reactive[list[IgnoreFile]] = reactive(get_gitignore_templates())
    filtered_ignore_files: reactive[list[IgnoreFile]] = reactive([])
    search_name: reactive[str] = reactive("")

    highlighted_ignore_file: reactive[IgnoreFile | None] = reactive(None)

    @on(Button.Pressed, selector="#search-button")
    @on(Input.Submitted, selector="#search-input")
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
            file
            for file in self.ignore_files
            if self.search_name.lower() in file.language.lower()
        ]

    def watch_filtered_ignore_files(self: Self, ignore_files: list[IgnoreFile]) -> None:
        ignore_list = self.query_one("#ignore-list", expect_type=LanguageList)
        ignore_list.clear_options()

        if ignore_files:
            ignore_list.add_options(
                [Option(file, id=file.id) for file in ignore_files],
            )
            ignore_list.border_title = (
                f"{ignore_list.DEFAULT_BORDER_TITLE} ({ignore_list.option_count})"
            )
        else:
            ignore_list.add_option(Option("No files found", disabled=True))
            ignore_list.border_title = f"{ignore_list.DEFAULT_BORDER_TITLE}"

    def compose(self: Self) -> ComposeResult:
        with Horizontal(id="search-container"):
            yield Input(
                placeholder="Language...",
                type="text",
                id="search-input",
            )
            yield SearchButton("Search", id="search-button")
        with Horizontal(id="ignore-container"):
            yield LanguageList(id="ignore-list")
            yield FilePreview(id="ignore-code").data_bind(
                SearchForm.highlighted_ignore_file,
            )
