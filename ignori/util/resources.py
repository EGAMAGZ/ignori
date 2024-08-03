import importlib.resources as resources
from pathlib import Path


def get_path_from_resource_dir(dir_name: str) -> Path:
    with resources.path("ignori", dir_name) as path:
        return path
