from typing import Self

from textual.binding import Binding
from textual.widgets import OptionList

from ignori.screens.modals.info_modal import InfoModal
from ignori.util.explorer import open_file_explorer
from ignori.util.settings import TEMPLATES_PATH


class LanguageList(OptionList):
    DEFAULT_BORDER_TITLE = "Languages"
    BINDINGS = [
        Binding("ctrl+o", "open_templates", "Open explorer", show=True),
    ]
    BORDER_TITLE = DEFAULT_BORDER_TITLE

    def action_open_templates(self: Self) -> None:
        try:
            open_file_explorer(TEMPLATES_PATH)
        except ValueError as error:
            error_message = str(error)
            self.app.push_screen(InfoModal(error_message))
