from dataclasses import dataclass, field

from src.engine.rules import EMPTY, PLAYER_BLUE


@dataclass
class GameState:
    grid_size: int = 5
    board: list[list[int]] = field(init=False)
    dots: list[list[int]] = field(init=False)
    current_player: int = PLAYER_BLUE
    turn_count: int = 0
    winner: int | None = None
    blue_has_initialized: bool = False
    red_has_initialized: bool = False

    def __post_init__(self):
        self.board = [[EMPTY for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.dots = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
