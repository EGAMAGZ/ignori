from pathlib import Path

import pytest


@pytest.fixture(scope="package")
def generated_file(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("output") / ".gitignore"
