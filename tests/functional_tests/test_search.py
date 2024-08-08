import pytest
from textual.widgets import Input

from ignori.app import IgnoriApp
from ignori.util.file import get_gitignore_templates
from ignori.widgets.language_list import LanguageList


@pytest.mark.asyncio
async def test_empty_search() -> None:
    app = IgnoriApp()
    async with app.run_test() as pilot:
        search_input = pilot.app.query_one("#search-input", expect_type=Input)
        search_input.focus()
        await pilot.click("#search-button")

        language_list = pilot.app.query_one("#ignore-list", expect_type=LanguageList)
        assert language_list.option_count == len(get_gitignore_templates())


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "language, option_count",
    [("py", 2), ("python", 1), ("c++", 1), ("c", 52), ("java", 1)],
)
async def test_languages_search(language: str, option_count: int) -> None:
    app = IgnoriApp()
    async with app.run_test() as pilot:
        search_input = pilot.app.query_one("#search-input", expect_type=Input)
        search_input.focus()
        await pilot.press(*language)
        await pilot.click("#search-button")

        language_list = pilot.app.query_one("#ignore-list", expect_type=LanguageList)
        assert language_list.option_count == option_count


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "language, option_count",
    [("python", 1), ("PyThOn", 1), ("PYTHON", 1)],
)
async def test_search_with_different_capitalization(
    language: str,
    option_count: int,
) -> None:
    app = IgnoriApp()
    async with app.run_test() as pilot:
        search_input = pilot.app.query_one("#search-input", expect_type=Input)
        search_input.focus()
        await pilot.press(*language)
        await pilot.click("#search-button")

        language_list = pilot.app.query_one("#ignore-list", expect_type=LanguageList)
        assert language_list.option_count == option_count
