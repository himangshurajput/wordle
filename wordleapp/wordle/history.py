"""Persistence of finished games to a JSON file."""

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from wordle.game import Game, GameStatus


@dataclass(frozen=True)
class GameRecord:
    """A summary of one finished game.

    Attributes:
        solution: The word the player was trying to find.
        guesses: Every guess submitted, in order.
        won: Whether the player found the word.
    """

    solution: str
    guesses: list[str]
    won: bool

    @classmethod
    def from_game(cls, game: Game) -> "GameRecord":
        """Build a record from a finished game.

        Args:
            game: A game that has been won or lost.

        Returns:
            The record describing the game.

        Raises:
            ValueError: If the game is still in progress.
        """
        if not game.is_over:
            msg = "cannot record a game that is still in progress"
            raise ValueError(msg)
        return cls(
            solution=game.solution,
            guesses=[result.guess for result in game.results],
            won=game.status is GameStatus.WON,
        )


class GameHistory:
    """A list of finished games stored in a JSON file across sessions."""

    def __init__(self, path: Path) -> None:
        """Load any records already stored at ``path``.

        Args:
            path: Location of the JSON file. It is created on first save.

        Raises:
            ValueError: If the file exists but is not valid history data.
        """
        self.path = path
        self.records: list[GameRecord] = []
        if path.exists():
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.records = [GameRecord(**item) for item in payload]
            except (json.JSONDecodeError, TypeError) as exc:
                msg = f"could not read history at {path}: {exc}"
                raise ValueError(msg) from exc

    def add(self, game: Game) -> None:
        """Record a finished game and write the history to disk.

        Args:
            game: A game that has been won or lost.
        """
        self.records.append(GameRecord.from_game(game))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [asdict(record) for record in self.records]
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @property
    def games_played(self) -> int:
        """Return the number of stored games."""
        return len(self.records)

    @property
    def games_won(self) -> int:
        """Return how many stored games were won."""
        return sum(record.won for record in self.records)
