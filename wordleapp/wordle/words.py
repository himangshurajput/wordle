"""Loading and validation of the word list."""

from pathlib import Path

WORD_LENGTH = 5


def load_words(path: Path, word_length: int = WORD_LENGTH) -> frozenset[str]:
    """Read one word per line from a text file and validate every entry.

    Args:
        path: Location of the text file.
        word_length: Number of letters each word must have.

    Returns:
        The distinct lowercase words in the file.

    Raises:
        ValueError: If the file is empty or contains a malformed word.
    """
    words: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        word = line.strip().lower()
        if not word:
            continue
        if len(word) != word_length:
            msg = f"{word!r} has {len(word)} letters; expected {word_length}"
            raise ValueError(msg)
        if not word.isalpha():
            msg = f"{word!r} contains non-letter characters"
            raise ValueError(msg)
        words.add(word)
    if not words:
        msg = f"no words found in {path}"
        raise ValueError(msg)
    return frozenset(words)
