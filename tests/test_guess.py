import pytest

from wordle.guess import LetterStatus, evaluate_guess

C = LetterStatus.CORRECT
P = LetterStatus.PRESENT
A = LetterStatus.ABSENT


def statuses(guess: str, solution: str) -> tuple[LetterStatus, ...]:
    return evaluate_guess(guess, solution).statuses


def test_all_correct():
    assert statuses("crane", "crane") == (C, C, C, C, C)


def test_all_absent():
    assert statuses("world", "abbey") == (A, A, A, A, A)


def test_present_letters_in_wrong_positions():
    assert statuses("trace", "crane") == (A, C, C, P, C)


def test_duplicate_in_guess_single_in_solution_marks_only_first():
    assert statuses("speed", "abide") == (A, A, P, A, P)


def test_correct_copy_is_claimed_before_present_copies():
    assert statuses("geese", "steel") == (A, P, C, P, A)


def test_guess_has_more_copies_than_solution():
    assert statuses("eerie", "steel") == (P, P, A, A, A)


def test_extra_copies_are_absent_once_solution_copies_are_used():
    assert statuses("banal", "nanny") == (A, C, C, A, A)


def test_triple_letter_guess_against_triple_letter_solution():
    assert statuses("geese", "eerie") == (A, C, P, A, C)


def test_solution_with_repeats_guess_without():
    assert statuses("slate", "steel") == (C, P, A, P, P)


def test_mixed_correct_and_present_duplicates():
    assert statuses("allee", "level") == (A, P, P, C, P)


def test_length_mismatch_raises():
    with pytest.raises(ValueError):
        evaluate_guess("abc", "crane")


def test_is_correct_only_when_all_green():
    assert evaluate_guess("crane", "crane").is_correct
    assert not evaluate_guess("trace", "crane").is_correct


def test_render_produces_one_square_per_letter():
    assert evaluate_guess("trace", "crane").render() == "⬜🟩🟩🟨🟩"
