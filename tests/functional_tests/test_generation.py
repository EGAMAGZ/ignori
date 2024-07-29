from pathlib import Path

import pytest

from ignori.app import IgnoriApp
from ignori.ignore_file import IgnoreFile
from ignori.widgets.input import BorderlessInput
from ignori.widgets.language_badge import LanguageBadge
from ignori.widgets.language_list import LanguageList


@pytest.mark.asyncio
@pytest.mark.parametrize("language", ["Python", "Java", "Kotlin"])
async def test_language_selection(language: str, data_dir: Path) -> None:
    app = IgnoriApp()
    async with app.run_test() as pilot:
        ignore_file = IgnoreFile(data_dir / "unit_tests" / f"{language}.gitignore")

        search_input = pilot.app.query_one("#search-input", expect_type=BorderlessInput)
        search_input.focus()
        await pilot.press(*language)
        await pilot.click("#search-button")

        language_list: LanguageList = pilot.app.query_one(
            "#ignore-list",
            expect_type=LanguageList,
        )
        language_list.focus()

        for index in range(language_list.option_count):
            option = language_list.get_option_at_index(index)

            await pilot.press("down")
            if option.id == ignore_file.id:
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
        ["Kotlin", "Python"],
    ],
)
async def test_language_selection_and_unselection(
    languages: list[str],
    data_dir: Path,
) -> None:
    app = IgnoriApp()
    async with app.run_test() as pilot:
        for language in languages:
            ignore_file = IgnoreFile(data_dir / "unit_tests" / f"{language}.gitignore")

            search_input = pilot.app.query_one(
                "#search-input",
                expect_type=BorderlessInput,
            )
            search_input.clear()
            search_input.focus()

            await pilot.press(*language)
            await pilot.click("#search-button")

            language_list: LanguageList = pilot.app.query_one(
                "#ignore-list",
                expect_type=LanguageList,
            )
            language_list.focus()

            for index in range(language_list.option_count):
                option = language_list.get_option_at_index(index)

                await pilot.press("down")
                if option.id == ignore_file.id:
                    await pilot.press("enter")

            language_badge: LanguageBadge = pilot.app.query_one(
                "#language-badge",
                expect_type=LanguageBadge,
            )

            assert language_badge.language_selected is not None
            assert language_badge.language_selected.language == language
