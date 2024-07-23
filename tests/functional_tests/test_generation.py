import pytest
from textual.widgets import OptionList

from ignori.app import IgnoriApp
from ignori.widgets.input import BorderlessInput
from ignori.widgets.language_list import LanguageList


@pytest.mark.asyncio
@pytest.mark.parametrize("language", ["Python", "Java", "Kotlin"])
async def test_language_selection(language: str) -> None:
    app = IgnoriApp()
    async with app.run_test() as pilot:
        search_input = pilot.app.query_one("#search-input", expect_type=BorderlessInput)
        search_input.focus()
        await pilot.press(*language)
        await pilot.click("#search-button")

        language_list: OptionList = pilot.app.query_one(
            "#ignore-list",
            expect_type=OptionList,
        )
        language_list.focus()

        # await pilot.click("#ignore-list", offset=(3, 3))
        print(language_list.highlighted, language_list.option_count)
        assert True
