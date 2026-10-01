from pathlib import Path

import pytest

from wordle.words import load_words


def test_loads_every_word(words_file: Path):
    loaded = load_words(words_file)
    assert len(loaded) == 15
    assert "crane" in loaded


def test_words_are_lowercased_and_stripped(tmp_path: Path):
    path = tmp_path / "words.txt"
    path.write_text("  CRANE \n\nslate\n   \n", encoding="utf-8")
    assert load_words(path) == frozenset({"crane", "slate"})


def test_duplicates_are_collapsed(tmp_path: Path):
    path = tmp_path / "words.txt"
    path.write_text("crane\nCRANE\ncrane\n", encoding="utf-8")
    assert len(load_words(path)) == 1


def test_wrong_length_word_rejected(tmp_path: Path):
    path = tmp_path / "words.txt"
    path.write_text("crane\ncranes\n", encoding="utf-8")
    with pytest.raises(ValueError, match="expected 5"):
        load_words(path)


def test_non_letter_word_rejected(tmp_path: Path):
    path = tmp_path / "words.txt"
    path.write_text("cr4ne\n", encoding="utf-8")
    with pytest.raises(ValueError, match="non-letter"):
        load_words(path)


def test_empty_file_rejected(tmp_path: Path):
    path = tmp_path / "words.txt"
    path.write_text("\n\n", encoding="utf-8")
    with pytest.raises(ValueError, match="no words"):
        load_words(path)


def test_missing_file_raises_os_error(tmp_path: Path):
    with pytest.raises(OSError):
        load_words(tmp_path / "missing.txt")


def test_bundled_word_list_is_valid():
    path = Path(__file__).resolve().parent.parent / "data" / "words.txt"
    assert len(load_words(path)) > 100
