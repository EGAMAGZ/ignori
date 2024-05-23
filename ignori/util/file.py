from ignori.ignore_file import IgnoreFile
from ignori.util.settings import TEMPLATES_PATH


def search_files_by_name(template_name: str | None = None) -> list[IgnoreFile]:
    template_files = [
        IgnoreFile(file)
        for file in TEMPLATES_PATH.iterdir()
        if template_name is None or template_name.lower() in file.stem.lower()
    ]

    return sorted(template_files, key=lambda file: file.language)
