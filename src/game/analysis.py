"""Lightweight gameplay analysis helpers for HUD statistics."""

from src.controller import get_scores
from src.engine.rules import PLAYER_BLUE, PLAYER_RED


def _sum_dots(state, owner):
    total = 0
    for row in range(state.grid_size):
        for col in range(state.grid_size):
            if state.board[row][col] == owner:
                total += state.dots[row][col]
    return total


def estimate_win_chances(state):
    """Estimate blue/red win chances from territory, dots, and move access."""
    blue_cells, red_cells = get_scores(state)
    blue_dots = _sum_dots(state, PLAYER_BLUE)
    red_dots = _sum_dots(state, PLAYER_RED)

    blue_pressure = blue_cells * 1.45 + blue_dots * 0.35
    red_pressure = red_cells * 1.45 + red_dots * 0.35

    if blue_pressure == 0 and red_pressure == 0:
        return 50.0, 50.0

    total = blue_pressure + red_pressure
    blue_chance = (blue_pressure / total) * 100.0
    red_chance = 100.0 - blue_chance
    return round(blue_chance, 1), round(red_chance, 1)


def format_cell_label(row, col):
    """Render a board coordinate as A1 style label."""
    if row is None or col is None:
        return "-"
    return f"{chr(ord('A') + col)}{row + 1}"