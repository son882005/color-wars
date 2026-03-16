import random

from src.engine.explosion import resolve_explosions
from src.engine.rules import PLAYER_BLUE, PLAYER_RED, get_move_dot_increment, get_valid_moves


def evaluate(board):
    score = 0

    for row in board:
        for cell in row:
            if cell == PLAYER_RED:
                score += 1
            elif cell == PLAYER_BLUE:
                score -= 1

    return score


def get_ai_move(board, dots):
    moves = get_valid_moves(board, PLAYER_RED)
    if not moves:
        return None

    no_ai_cells = not any(cell == PLAYER_RED for row in board for cell in row)
    if no_ai_cells:
        return random.choice(moves)

    best_score = -9999
    best_move = None

    for row, col in moves:
        board_copy = [line[:] for line in board]
        dots_copy = [line[:] for line in dots]

        increment = get_move_dot_increment(board_copy, row, col)
        board_copy[row][col] = PLAYER_RED
        dots_copy[row][col] += increment

        resolve_explosions(board_copy, dots_copy, row, col)

        score = evaluate(board_copy)

        if score > best_score:
            best_score = score
            best_move = (row, col)

    return best_move
