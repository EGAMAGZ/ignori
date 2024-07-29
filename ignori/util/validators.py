from pathlib import Path

from textual.validation import ValidationResult, Validator
from typing_extensions import Self


class PathValidator(Validator):
    def validate(self: Self, value: str) -> ValidationResult:
        if not self.validate_path(value):
            return self.failure("Path does not exist or is not a directory")
        return self.success()

    @staticmethod
    def validate_path(value: str) -> bool:
        path = Path(value)
        return path.exists() and path.is_dir()
