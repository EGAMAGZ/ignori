import platform
import subprocess
from pathlib import Path


def open_file_explorer(path: Path) -> None:
    system = platform.system().lower()
    match system:
        case "windows":
            subprocess.run(["explorer", path])

        case "linux":
            subprocess.run(["xdg-open", path])

        case "darwin":
            subprocess.run(["open", path])

        case _:
            raise ValueError(f"Unsupported system: {system}")
