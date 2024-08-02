from dataclasses import dataclass, field
from itertools import cycle
from pathlib import Path
from typing import Self

from rich.console import Console, ConsoleOptions, RenderResult


@dataclass
class IgnoreFile:
    id: str = field(init=False)
    path: Path
    language: str = field(init=False)
    categories: list[str] = field(default_factory=list)

    def __post_init__(self: Self) -> None:
        self.language = self.path.stem
        self.id = "-".join(
            [
                self.language.lower(),
                *self.categories,
            ],
        )

    def __rich_console__(
        self: Self,
        console: Console,
        options: ConsoleOptions,
    ) -> RenderResult:
        categories_colors = cycle(
            [
                "white on red",
                "white on blue",
                "black on green",
                "black on yellow",
            ],
        )
        categories = " ".join(
            [
                f"[{(color:=next(categories_colors))}]{category}[/{color}]"
                for category in self.categories
            ],
        )
        yield f"{self.language} {categories}" if categories else f"{self.language}"


def get_option_by_id(
    ignore_files: list[IgnoreFile],
    option_id: str,
) -> IgnoreFile | None:
    selected_file = next(
        (file for file in ignore_files if file.id == option_id),
        None,
    )
    return selected_file
