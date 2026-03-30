import math
import random

from src.engine.explosion import resolve_explosions
from src.engine.rules import PLAYER_BLUE, PLAYER_RED, get_move_dot_increment, get_valid_moves


def _material_score(board):
    score = 0
    for row in board:
        for cell in row:
            if cell == PLAYER_RED:
                score += 1
            elif cell == PLAYER_BLUE:
                score -= 1
    return score


def _mobility_score(board):
    red_moves = len(get_valid_moves(board, PLAYER_RED))
    blue_moves = len(get_valid_moves(board, PLAYER_BLUE))
    return red_moves - blue_moves


def evaluate_board(board, dots):
    """Evaluate board state for Red (AI). Higher score means better for AI."""
    material = _material_score(board)
    mobility = _mobility_score(board)

    red_dots = 0
    blue_dots = 0
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == PLAYER_RED:
                red_dots += dots[r][c]
            elif board[r][c] == PLAYER_BLUE:
                blue_dots += dots[r][c]

    return material * 3.0 + mobility * 1.5 + (red_dots - blue_dots) * 0.2


def simulate_move(board, dots, move):
    """Return a copied board/dots after applying move for Red and resolving chain explosions."""
    row, col = move
    board_copy = [line[:] for line in board]
    dots_copy = [line[:] for line in dots]

    increment = get_move_dot_increment(board_copy, row, col)
    board_copy[row][col] = PLAYER_RED
    dots_copy[row][col] += increment
    resolve_explosions(board_copy, dots_copy, row, col)

    return board_copy, dots_copy


def get_move_score(board, dots, move):
    next_board, next_dots = simulate_move(board, dots, move)
    return evaluate_board(next_board, next_dots)


def get_top_moves(board, dots, top_n=3):
    moves = get_valid_moves(board, PLAYER_RED)
    if not moves:
        return []

    move_scores = [(move, get_move_score(board, dots, move)) for move in moves]
    move_scores.sort(key=lambda item: item[1], reverse=True)

    return move_scores[: min(top_n, len(move_scores))]


def softmax_selection(scored_moves, temperature=0.8):
    """Pick one move from scored candidates via softmax probabilities."""
    if not scored_moves:
        return None

    if temperature <= 0:
        return scored_moves[0][0]

    scores = [score for _, score in scored_moves]
    max_score = max(scores)
    weights = [math.exp((score - max_score) / temperature) for score in scores]

    return random.choices([move for move, _ in scored_moves], weights=weights, k=1)[0]


def get_med_move(board, dots):
    """Medium AI: evaluate candidates, keep top moves, then choose by softmax."""
    top_scored = get_top_moves(board, dots, top_n=3)
    return softmax_selection(top_scored)
