from importlib.metadata import version
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

STYLES_DIR = BASE_DIR / "styles"

STYLES_PATH = [
    STYLES_DIR / "global.tcss",
    STYLES_DIR / "widgets.tcss",
    STYLES_DIR / "modals.tcss",
]

TEMPLATES_PATH = BASE_DIR / "templates"

APP_TITLE = "Ignori"

APP_VERSION = version("ignori")

DEFAULT_OUTPUT_FILE = ".gitignore"
