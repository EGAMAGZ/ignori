from textual.widgets import Input


class BorderlessInput(Input):
    DEFAULT_CSS = """\
    BorderlessInput{
        border: none;
        width: 1fr;
        height: 1;

        &:focus {
            border: none !important;
            height: 1 !important;
        }
        & > .input--cursor {
            color: $text;
            background: $accent-lighten-2;
        }
        &.-invalid {
            border: none !important;
            height: 1;
            background: red 10%;
            color: $text;
        }
    }
    """
