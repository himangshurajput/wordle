"""Terminal front end for the game."""

import random
from pathlib import Path

from wordle.exceptions import WordleError
from wordle.game import Game, GameStatus
from wordle.history import GameHistory
from wordle.words import load_words

WORDS_PATH = Path(__file__).resolve().parent.parent / "data" / "words.txt"
HISTORY_PATH = Path.home() / ".wordle" / "history.json"


def play(game: Game) -> None:
    """Prompt for guesses until the game is won or lost."""
    print(f"Guess the {len(game.solution)}-letter word. You have {game.max_attempts} attempts.")
    while not game.is_over:
        try:
            result = game.guess(input(f"[{game.attempts_used + 1}/{game.max_attempts}] > "))
        except WordleError as exc:
            print(exc)
            continue
        except EOFError:
            print()
            return
        print(f"{result.render()}  {result.guess.upper()}")
    if game.status is GameStatus.WON:
        print(f"You won in {game.attempts_used} attempt(s)!")
    else:
        print(f"Out of attempts. The word was {game.solution.upper()}.")


def main() -> int:
    """Load the words and history, play one game, and store the outcome."""
    try:
        words = load_words(WORDS_PATH)
        history = GameHistory(HISTORY_PATH)
    except (OSError, ValueError) as exc:
        print(exc)
        return 1
    game = Game(random.choice(sorted(words)), words)
    play(game)
    if game.is_over:
        history.add(game)
        print(f"Games played: {history.games_played}, won: {history.games_won}")
    return 0
