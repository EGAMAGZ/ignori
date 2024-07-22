from pathlib import Path

import pytest

from ignori.util.file import copy_file_content


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
