import pytest

from ignori.app import IgnoriApp
from ignori.widgets.input import BorderlessInput
from ignori.widgets.language_badge import LanguageBadge
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

        language_list: LanguageList = pilot.app.query_one(
            "#ignore-list",
            expect_type=LanguageList,
        )
        language_list.focus()

        # FIXME: Improve option selection to be independent of the list order
        await pilot.press("down")
        await pilot.press("enter")

        language_badge: LanguageBadge = pilot.app.query_one(
            "#language-badge",
            expect_type=LanguageBadge,
        )

        assert language_badge.language_selected is not None
        assert language_badge.language_selected.language == language


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "languages",
    [
        ["Python", "Kotlin"],
    ],
)
async def test_language_selection_and_unselection(languages: list[str]) -> None:
    pass
