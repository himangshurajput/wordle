"""Guess evaluation, including correct handling of repeated letters."""

from collections import Counter
from dataclasses import dataclass
from enum import Enum


class LetterStatus(Enum):
    """Feedback for a single letter of a guess."""

    CORRECT = "🟩"
    PRESENT = "🟨"
    ABSENT = "⬜"


@dataclass(frozen=True)
class GuessResult:
    """The outcome of comparing one guess against the solution.

    Attributes:
        guess: The guessed word in lowercase.
        statuses: One status per letter, in order.
    """

    guess: str
    statuses: tuple[LetterStatus, ...]

    @property
    def is_correct(self) -> bool:
        """Return True when every letter is in the right place."""
        return all(status is LetterStatus.CORRECT for status in self.statuses)

    def render(self) -> str:
        """Return the feedback as a row of coloured squares."""
        return "".join(status.value for status in self.statuses)


def evaluate_guess(guess: str, solution: str) -> GuessResult:
    """Compare a guess with the solution letter by letter.

    Exact matches are marked first. Each remaining guess letter is then marked
    present only while the solution still has an unclaimed copy of it, so a
    letter never receives more marks than the solution contains.

    Args:
        guess: The guessed word.
        solution: The target word.

    Returns:
        Feedback for every letter of the guess.

    Raises:
        ValueError: If the two words differ in length.
    """
    if len(guess) != len(solution):
        msg = "guess and solution must have the same length"
        raise ValueError(msg)

    statuses = [LetterStatus.ABSENT] * len(guess)
    unclaimed: Counter[str] = Counter()

    for index, (guessed, actual) in enumerate(zip(guess, solution, strict=True)):
        if guessed == actual:
            statuses[index] = LetterStatus.CORRECT
        else:
            unclaimed[actual] += 1

    for index, guessed in enumerate(guess):
        if statuses[index] is LetterStatus.ABSENT and unclaimed[guessed] > 0:
            statuses[index] = LetterStatus.PRESENT
            unclaimed[guessed] -= 1

    return GuessResult(guess=guess, statuses=tuple(statuses))
