from pathlib import Path

import pytest

from ignori.util.validators import PathValidator


@pytest.mark.parametrize(
    "dir_path, is_valid",
    [("Example.gitignore", False), ("category1", True)],
)
def test_path_validator(dir_path: Path, is_valid: bool, data_dir: Path) -> None:
    path = data_dir / "unit_tests" / dir_path

    validator = PathValidator()
    validation_result = validator.validate(str(path))

    assert validation_result.is_valid == is_valid
