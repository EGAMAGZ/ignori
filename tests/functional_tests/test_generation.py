from pathlib import Path

import pytest
from textual.notifications import Notification, Notifications
from textual.widgets import Input

from ignori.app import IgnoriApp
from ignori.ignore_file import IgnoreFile
from ignori.widgets.language_badge import LanguageBadge
from ignori.widgets.language_list import LanguageList


@pytest.mark.asyncio
@pytest.mark.parametrize("language", ["Python", "Java", "Kotlin"])
async def test_language_selection(language: str, data_dir: Path) -> None:
    app = IgnoriApp()
    async with app.run_test() as pilot:
        ignore_file = IgnoreFile(data_dir / "unit_tests" / f"{language}.gitignore")

        search_input = pilot.app.query_one("#search-input", expect_type=Input)
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
                expect_type=Input,
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


@pytest.mark.asyncio
@pytest.mark.parametrize("path", ["this/path/doesnt/exists"])
async def test_generation_without_language_selection(path: str) -> None:
    app = IgnoriApp()
    async with app.run_test() as pilot:
        path_input = pilot.app.query_one("#path-input", expect_type=Input)
        path_input.focus()

        await pilot.press(*path)
        await pilot.click("#path-button")

        path_input = pilot.app.query_one("#path-input", expect_type=Input)

        notifications: Notifications = pilot.app._notifications  # noqa

        assert not path_input.is_valid
        assert len(notifications) == 1

        last_notification: Notification = (
            list(notifications._notifications.values())[-1]  # noqa
        )

        assert last_notification.title == "Error"
        assert last_notification.message == "Path does not exist or is not a directory"


@pytest.mark.asyncio
async def test_generation_with_invalid_output_path() -> None:
    app = IgnoriApp()
    async with app.run_test() as pilot:
        notifications = pilot.app._notifications  # noqa
        await pilot.click("#path-button")

        assert len(notifications) == 1
        last_notification: Notification = (
            list(notifications._notifications.values())[-1]  # noqa
        )

        assert last_notification.title == "Error"
        assert last_notification.message == "No language selected"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "language",
    [
        "Python",
    ],
)
async def test_ignore_generation(
    language: str,
    generated_file: Path,
    templates_dir: Path,
) -> None:
    app = IgnoriApp()

    async with app.run_test() as pilot:
        source_file = templates_dir / f"{language}.gitignore"
        generated_file_dir = str(generated_file.parent)
        ignore_file = IgnoreFile(source_file)

        search_input = pilot.app.query_one(
            "#search-input",
            expect_type=Input,
        )
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

        path_input = pilot.app.query_one("#path-input", expect_type=Input)
        path_input.focus()

        await pilot.press(*generated_file_dir)
        await pilot.click("#path-button")

        path_input = pilot.app.query_one("#path-input", expect_type=Input)

        assert path_input.is_valid
        assert generated_file.read_text() == source_file.read_text()

        notifications = pilot.app._notifications  # noqa
        last_notification: Notification = (
            list(notifications._notifications.values())[-1]  # noqa
        )

        assert last_notification.title == "Success"
        assert last_notification.message == "File generated successfully"
