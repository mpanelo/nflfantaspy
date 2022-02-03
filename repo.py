import dacite
import json
import os

from dataclasses import asdict
from typing import TypeVar, Type


DATA_DIR = "data/"
T = TypeVar("T")


def exists(filename: str) -> bool:
    return os.path.isfile(_get_full_path(filename))


def commit(dataclass: Type, filename: str):
    data = asdict(dataclass)
    with open(_get_full_path(filename), "w") as f:
        json.dump(data, f, indent=4)


def read(filename: str, dataclass: Type[T]) -> T:
    data = _read_json_file(filename)
    return dacite.from_dict(dataclass, data)


def _read_json_file(filename: str):
    with open(_get_full_path(filename), "r") as f:
        return json.load(f)


def _get_full_path(filename) -> str:
    return os.path.join(DATA_DIR, filename)
