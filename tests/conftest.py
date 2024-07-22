from pathlib import Path

import pytest


@pytest.fixture
def data_dir() -> Path:
    tests_dir = Path(__file__)
    return tests_dir.parent / "data"
