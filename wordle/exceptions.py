"""Exceptions raised as part of normal game flow."""


class WordleError(Exception):
    """Base class for every error raised by the game."""


class InvalidGuessLengthError(WordleError):
    """Raised when a guess does not have the required number of letters."""


class WordNotInListError(WordleError):
    """Raised when a guess is not in the accepted word list."""


class GameOverError(WordleError):
    """Raised when a guess is submitted after the game has ended."""
