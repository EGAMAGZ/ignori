import pytest


@pytest.fixture(scope="module", autouse=True)
def cleanup(request: pytest.FixtureRequest) -> None:
    def delete_ignore_file() -> None:
        pass

    request.addfinalizer(delete_ignore_file)
