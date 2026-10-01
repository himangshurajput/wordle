"""State of a single round of Wordle."""

from enum import Enum

from wordle.exceptions import GameOverError, InvalidGuessLengthError, WordNotInListError
from wordle.guess import GuessResult, evaluate_guess

MAX_ATTEMPTS = 6


class GameStatus(Enum):
    """Whether a game is still running, won, or lost."""

    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"


class Game:
    """One round of Wordle against a fixed solution."""

    def __init__(
        self, solution: str, words: frozenset[str], max_attempts: int = MAX_ATTEMPTS
    ) -> None:
        """Start a game.

        Args:
            solution: The word to find. Must be in ``words``.
            words: Every word accepted as a guess.
            max_attempts: How many guesses the player gets.

        Raises:
            ValueError: If the solution is not in the word list.
        """
        if solution not in words:
            msg = f"solution {solution!r} is not in the word list"
            raise ValueError(msg)
        self.solution = solution
        self.words = words
        self.max_attempts = max_attempts
        self.results: list[GuessResult] = []

    @property
    def attempts_used(self) -> int:
        """Return how many guesses have been submitted."""
        return len(self.results)

    @property
    def status(self) -> GameStatus:
        """Return the current lifecycle state of the game."""
        if self.results and self.results[-1].is_correct:
            return GameStatus.WON
        if len(self.results) >= self.max_attempts:
            return GameStatus.LOST
        return GameStatus.IN_PROGRESS

    @property
    def is_over(self) -> bool:
        """Return True once the game is won or lost."""
        return self.status is not GameStatus.IN_PROGRESS

    def guess(self, word: str) -> GuessResult:
        """Submit a guess and return its feedback.

        Args:
            word: The player's guess. Case and surrounding whitespace are ignored.

        Returns:
            Feedback for the guess.

        Raises:
            GameOverError: If the game has already ended.
            InvalidGuessLengthError: If the guess has the wrong number of letters.
            WordNotInListError: If the guess is not an accepted word.
        """
        if self.is_over:
            msg = f"the game is over; the word was {self.solution!r}"
            raise GameOverError(msg)
        cleaned = word.strip().lower()
        if len(cleaned) != len(self.solution):
            msg = f"{cleaned!r} has {len(cleaned)} letters; expected {len(self.solution)}"
            raise InvalidGuessLengthError(msg)
        if cleaned not in self.words:
            raise WordNotInListError(f"{cleaned!r} is not in the word list")
        result = evaluate_guess(cleaned, self.solution)
        self.results.append(result)
        return result
