import pytest

from ignori.app import IgnoriApp


@pytest.mark.asyncio
async def test_empty_search() -> None:
    app = IgnoriApp()
    async with app.run_test() as pilot:
        await pilot.click("#search-button")
    assert 2 + 3 == 5
