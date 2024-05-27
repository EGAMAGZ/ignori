from pathlib import Path

from ignori.ignore_file import IgnoreFile
from ignori.util.settings import TEMPLATES_PATH


def search_files_by_name(template_name: str = "") -> list[IgnoreFile]:
    template_files = [
        IgnoreFile(file)
        for file in TEMPLATES_PATH.iterdir()
        if template_name.lower() in file.stem.lower()
    ]

    return sorted(template_files, key=lambda file: file.language)


def copy_file_content(source_file: Path, destination_file: Path) -> None:
    with Path.open(source_file) as source, Path.open(
        destination_file,
        "w",
    ) as destination:
        destination.write(source.read())
