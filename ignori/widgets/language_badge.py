from typing import Self

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Label

from ignori.ignore_file import IgnoreFile


class LanguageBadge(
    Horizontal,
    can_focus=True,
    can_focus_children=False,
    inherit_bindings=False,
):
    DEFAULT_CSS = """\
    LanguageBadge {
        height: 1;
        width: auto;
        padding: 0 1;

        & #icon {
            padding: 0 1;
            background: white;
            color: $text;
        }
        & #language-name{

        }
    }

    LanguageBadge:focus {
        background: $primary;
    }
    """

    BINDINGS = [
        Binding("enter", "press", "Unselect languague", show=False),
    ]

    language_selected: reactive[IgnoreFile | None] = reactive(None)

    class Pressed(Message): ...


    def watch_language_selected(self: Self, ignore_file: IgnoreFile | None) -> None:
        language_name = self.query_one("#language-name", expect_type=Label)
        language_name.update(ignore_file.language if ignore_file else "No Language")

    def action_press(self: Self) -> None:
        self.post_message(self.Pressed())

    def compose(self: Self) -> ComposeResult:
        yield Label("X", id="icon")
        yield Label("LANGUAGE", id="language-name")
