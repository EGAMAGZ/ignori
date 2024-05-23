from dataclasses import dataclass, field
from pathlib import Path
from typing import Self


@dataclass
class IgnoreFile:
    id: str = field(init=False)
    path: Path
    language: str = field(init=False)

    def __post_init__(self: Self) -> None:
        self.language = self.path.stem
        self.id = self.language.lower()[:3]


if __name__ == "__main__":
    test_path = Path("Python.gitignore")
    ignore_file = IgnoreFile(test_path)
    assert ignore_file.language == "Python"
    assert ignore_file.id == "pyt"
