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
        background: $secondary-darken-3;

        &.no-language{
            background: $secondary-background;
            & #icon {
                display: none;
            }
        }

        & #icon {
            padding: 0 1;
            background: $secondary;
            color: $text;
        }

        & #language-name {
            color: $text;
            min-width: 10;
            padding: 0 1;
        }
    }

    LanguageBadge:focus {
        &.no-language {
            background: $secondary-darken-3;
        }

        & #icon {
            background: white;
            color: $text;
            text-style: bold;
        }
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

        self.set_class(ignore_file is None, "no-language")

    def action_press(self: Self) -> None:
        self.post_message(self.Pressed())

    def compose(self: Self) -> ComposeResult:
        yield Label("X", id="icon")
        yield Label("No language", id="language-name")
