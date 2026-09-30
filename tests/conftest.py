from pathlib import Path

import pytest

WORDS = [
    "abbey",
    "abide",
    "allee",
    "banal",
    "crane",
    "eerie",
    "geese",
    "level",
    "nanny",
    "robot",
    "slate",
    "speed",
    "steel",
    "trace",
    "world",
]


@pytest.fixture
def words() -> frozenset[str]:
    return frozenset(WORDS)


@pytest.fixture
def words_file(tmp_path: Path) -> Path:
    path = tmp_path / "words.txt"
    path.write_text("\n".join(WORDS) + "\n", encoding="utf-8")
    return path


@pytest.fixture
def history_path(tmp_path: Path) -> Path:
    return tmp_path / "history.json"
