from importlib.metadata import version

from ignori.util.resources import get_path_from_resource_dir

STYLES_DIR = get_path_from_resource_dir("styles")

STYLES = [
    STYLES_DIR / "global.tcss",
    STYLES_DIR / "widgets.tcss",
    STYLES_DIR / "modals.tcss",
]

TEMPLATES_PATH = get_path_from_resource_dir("templates")

APP_TITLE = "Ignori"

APP_VERSION = version("ignori")

DEFAULT_OUTPUT_FILE = ".gitignore"
