from dataclasses import dataclass, field
from pathlib import Path
from typing import Self


@dataclass
class IgnoreFile:
    id: str = field(init=False)
    path: Path
    language: str = field(init=False)
    categories: list[str] = field(default_factory=list)

    def __post_init__(self: Self) -> None:
        self.language = self.path.stem
        self.id = self.language.lower()

