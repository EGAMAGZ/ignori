from pathlib import Path

from ignori.ignore_file import IgnoreFile
from ignori.util.settings import TEMPLATES_PATH


def get_gitignore_templates() -> list[IgnoreFile]:
    template_files: list[IgnoreFile] = []
    current_categories: list[str] = []

    for path in TEMPLATES_PATH.iterdir():
        if path.is_dir():
            template_files.extend(
                __get_files(
                    template_subpath=path,
                    categories=current_categories,
                ),
            )

        else:
            template_files.append(
                IgnoreFile(
                    path=path,
                    categories=current_categories,
                ),
            )

    return sorted(template_files, key=lambda file: file.language)


def __get_files(template_subpath: Path, categories: list[str]) -> list[IgnoreFile]:
    template_files: list[IgnoreFile] = []

    current_categories: list[str] = [*categories, template_subpath.name]

    for path in template_subpath.iterdir():
        if path.is_dir():
            template_files.extend(
                __get_files(
                    template_subpath=path,
                    categories=current_categories,
                ),
            )

        else:
            template_files.append(
                IgnoreFile(
                    path=path,
                    categories=current_categories,
                ),
            )

    return template_files


def copy_file_content(
    *,
    source_file: Path,
    output_file: Path,
) -> None:
    with source_file.open("r") as source, output_file.open("w") as destination:
        destination.write(source.read())
