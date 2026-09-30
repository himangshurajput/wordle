import json
from pathlib import Path

import pytest

from wordle import cli


@pytest.fixture
def configured(monkeypatch: pytest.MonkeyPatch, words_file: Path, history_path: Path) -> Path:
    monkeypatch.setattr(cli, "WORDS_PATH", words_file)
    monkeypatch.setattr(cli, "HISTORY_PATH", history_path)
    monkeypatch.setattr(cli.random, "choice", lambda seq: "crane")
    return history_path


def test_full_game_is_recorded(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], configured: Path
):
    answers = iter(["cran", "zzzzz", "slate", "crane"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    assert cli.main() == 0
    out = capsys.readouterr().out
    assert "expected 5" in out
    assert "not in the word list" in out
    assert "You won in 2 attempt(s)!" in out
    assert "Games played: 1, won: 1" in out
    assert json.loads(configured.read_text(encoding="utf-8"))[0]["guesses"] == ["slate", "crane"]


def test_lost_game_reveals_solution(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], configured: Path
):
    monkeypatch.setattr("builtins.input", lambda prompt: "robot")
    assert cli.main() == 0
    assert "The word was CRANE." in capsys.readouterr().out


def test_end_of_input_abandons_game_without_recording(
    monkeypatch: pytest.MonkeyPatch, configured: Path
):
    def end_input(prompt: str) -> str:
        raise EOFError

    monkeypatch.setattr("builtins.input", end_input)
    assert cli.main() == 0
    assert not configured.exists()


def test_missing_word_file_returns_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
):
    monkeypatch.setattr(cli, "WORDS_PATH", tmp_path / "missing.txt")
    assert cli.main() == 1
    assert "missing.txt" in capsys.readouterr().out
