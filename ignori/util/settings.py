import tomllib
from pathlib import Path


def get_version() -> str:
    file_path = BASE_DIR / "pyproject.toml"

    with file_path.open("rb") as file:
        pyproject_data = tomllib.load(file)

    version: str = pyproject_data["tool"]["poetry"]["version"]
    return version


BASE_DIR = Path(__file__).resolve().parent.parent.parent

STYLES_DIR = BASE_DIR / "styles"

STYLES_PATH = [
    STYLES_DIR / "global.tcss",
    STYLES_DIR / "widgets.tcss",
    STYLES_DIR / "modals.tcss",
]

TEMPLATES_PATH = BASE_DIR / "templates"

APP_TITLE = "Ignori"

APP_VERSION = get_version()

DEFAULT_OUTPUT_FILE = ".gitignore"
