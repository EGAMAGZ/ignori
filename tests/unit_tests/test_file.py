from pathlib import Path

import pytest

from ignori.ignore_file import IgnoreFile
from ignori.util.file import copy_file_content, get_gitignore_templates


@pytest.mark.parametrize(
    "template,exists",
    [("Example.gitignore", False), ("Example2.gitignore", True)],
)
def test_copy_file_content(
    template: str,
    exists: bool,
    generated_file: Path,
    data_dir: Path,
) -> None:
    source_file = data_dir / "unit_tests" / template

    assert generated_file.exists() == exists

    copy_file_content(source_file=source_file, output_file=generated_file)
    with source_file.open() as source, generated_file.open() as output:
        assert source.read() == output.read()


def test_get_gitignore_templates(data_dir: Path) -> None:
    unit_test_dir = data_dir / "unit_tests"

    expected_templates: list[IgnoreFile] = sorted(
        [
            IgnoreFile(unit_test_dir / "Example.gitignore"),
            IgnoreFile(unit_test_dir / "Example2.gitignore"),
            IgnoreFile(
                unit_test_dir
                / "category1"
                / "category2"
                / "ExampleWithCategories.gitignore",
                categories=["category1", "category2"],
            ),
            IgnoreFile(
                unit_test_dir / "category1" / "ExampleWithCategory.gitignore",
                categories=["category1"],
            ),
        ],
        key=lambda file: file.language,
    )

    templates = get_gitignore_templates(unit_test_dir)

    assert len(templates) == len(expected_templates)
    assert templates == expected_templates
