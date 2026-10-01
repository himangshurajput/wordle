import pytest

from wordle.exceptions import GameOverError, InvalidGuessLengthError, WordNotInListError
from wordle.game import Game, GameStatus


def test_new_game_is_in_progress(words: frozenset[str]):
    game = Game("crane", words)
    assert game.status is GameStatus.IN_PROGRESS
    assert not game.is_over
    assert game.attempts_used == 0


def test_solution_must_be_in_word_list(words: frozenset[str]):
    with pytest.raises(ValueError):
        Game("zzzzz", words)


def test_correct_guess_wins(words: frozenset[str]):
    game = Game("crane", words)
    assert game.guess("crane").is_correct
    assert game.status is GameStatus.WON
    assert game.is_over


def test_guess_is_normalised(words: frozenset[str]):
    game = Game("crane", words)
    assert game.guess("  CRANE\n").is_correct


def test_running_out_of_attempts_loses(words: frozenset[str]):
    game = Game("crane", words, max_attempts=3)
    for _ in range(3):
        game.guess("robot")
    assert game.status is GameStatus.LOST
    assert game.is_over


def test_win_on_last_attempt_is_a_win(words: frozenset[str]):
    game = Game("crane", words, max_attempts=2)
    game.guess("robot")
    game.guess("crane")
    assert game.status is GameStatus.WON


def test_guess_after_win_raises(words: frozenset[str]):
    game = Game("crane", words)
    game.guess("crane")
    with pytest.raises(GameOverError):
        game.guess("slate")


def test_guess_after_loss_raises(words: frozenset[str]):
    game = Game("crane", words, max_attempts=1)
    game.guess("robot")
    with pytest.raises(GameOverError):
        game.guess("crane")


def test_wrong_length_guess_raises_without_using_attempt(words: frozenset[str]):
    game = Game("crane", words)
    with pytest.raises(InvalidGuessLengthError):
        game.guess("cran")
    assert game.attempts_used == 0


def test_unknown_word_raises_without_using_attempt(words: frozenset[str]):
    game = Game("crane", words)
    with pytest.raises(WordNotInListError):
        game.guess("zzzzz")
    assert game.attempts_used == 0


def test_length_is_checked_before_word_list(words: frozenset[str]):
    game = Game("crane", words)
    with pytest.raises(InvalidGuessLengthError):
        game.guess("cranes")


def test_results_are_kept_in_order(words: frozenset[str]):
    game = Game("crane", words)
    game.guess("slate")
    game.guess("trace")
    assert [result.guess for result in game.results] == ["slate", "trace"]
