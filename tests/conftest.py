from pathlib import Path

import pytest


@pytest.fixture
def data_dir() -> Path:
    tests_dir = Path(__file__)
    return tests_dir.parent / "data"


@pytest.fixture
def templates_dir() -> Path:
    test_dir = Path(__file__)
    return test_dir.parent.parent / "templates"


@pytest.fixture(scope="module")
def generated_file(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("output") / ".gitignore"
