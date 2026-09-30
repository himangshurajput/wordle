import json
from pathlib import Path

import pytest

from wordle.game import Game
from wordle.history import GameHistory, GameRecord


def finished(words: frozenset[str], solution: str, guesses: list[str], attempts: int = 6) -> Game:
    game = Game(solution, words, max_attempts=attempts)
    for guess in guesses:
        game.guess(guess)
    return game


def test_missing_file_gives_empty_history(history_path: Path):
    history = GameHistory(history_path)
    assert history.games_played == 0
    assert not history_path.exists()


def test_record_from_unfinished_game_raises(words: frozenset[str]):
    with pytest.raises(ValueError):
        GameRecord.from_game(Game("crane", words))


def test_record_captures_outcome(words: frozenset[str]):
    record = GameRecord.from_game(finished(words, "crane", ["slate", "crane"]))
    assert record == GameRecord(solution="crane", guesses=["slate", "crane"], won=True)


def test_add_writes_json_file(words: frozenset[str], history_path: Path):
    GameHistory(history_path).add(finished(words, "crane", ["crane"]))
    payload = json.loads(history_path.read_text(encoding="utf-8"))
    assert payload == [{"solution": "crane", "guesses": ["crane"], "won": True}]


def test_history_survives_across_sessions(words: frozenset[str], history_path: Path):
    first = GameHistory(history_path)
    first.add(finished(words, "crane", ["crane"]))
    first.add(finished(words, "slate", ["robot"], attempts=1))
    second = GameHistory(history_path)
    assert second.games_played == 2
    assert second.games_won == 1
    assert second.records[1].guesses == ["robot"]


def test_parent_directories_are_created(words: frozenset[str], tmp_path: Path):
    path = tmp_path / "nested" / "history.json"
    GameHistory(path).add(finished(words, "crane", ["crane"]))
    assert path.exists()


def test_corrupt_json_raises(history_path: Path):
    history_path.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError):
        GameHistory(history_path)


def test_malformed_record_raises(history_path: Path):
    history_path.write_text('[{"solution": "crane"}]', encoding="utf-8")
    with pytest.raises(ValueError):
        GameHistory(history_path)
