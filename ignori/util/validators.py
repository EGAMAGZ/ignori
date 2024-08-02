from pathlib import Path
from typing import Self

from textual.validation import ValidationResult, Validator


class PathValidator(Validator):
    def validate(self: Self, value: str) -> ValidationResult:
        if not self.validate_path(value):
            return self.failure("Path does not exist or is not a directory")
        return self.success()

    @staticmethod
    def validate_path(value: str) -> bool:
        path = Path(value)
        return path.exists() and path.is_dir()
