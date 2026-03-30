import random
import time

from src.engine.explosion import resolve_explosions
from src.engine.rules import PLAYER_BLUE, PLAYER_RED, get_move_dot_increment, get_valid_moves

INF = 10**9
MAX_DEPTH = 4
MAX_THINK_TIME_SEC = 0.045
ROOT_TOP_K = 8
INNER_TOP_K = 6
NOISE_SCORE_DIFF = 0.08

_TRANSPOSITION_TABLE = {}


def _state_key(board, dots, player, depth):
    board_key = tuple(tuple(row) for row in board)
    dots_key = tuple(tuple(row) for row in dots)
    return board_key, dots_key, player, depth


def _simulate_move(board, dots, move, player):
    row, col = move
    board_copy = [line[:] for line in board]
    dots_copy = [line[:] for line in dots]

    inc = get_move_dot_increment(board_copy, row, col)
    board_copy[row][col] = player
    dots_copy[row][col] += inc
    resolve_explosions(board_copy, dots_copy, row, col)
    return board_copy, dots_copy


def _normalized_features(board, dots):
    size = len(board)
    total = max(1, size * size)

    red_cells = 0
    blue_cells = 0
    red_dots = 0
    blue_dots = 0
    red_threat = 0
    blue_threat = 0
    red_stable = 0
    blue_stable = 0

    for r in range(size):
        for c in range(size):
            cell = board[r][c]
            dot = dots[r][c]
            if cell == PLAYER_RED:
                red_cells += 1
                red_dots += dot
                if dot >= 3:
                    red_threat += 1
                if dot <= 1:
                    red_stable += 1
            elif cell == PLAYER_BLUE:
                blue_cells += 1
                blue_dots += dot
                if dot >= 3:
                    blue_threat += 1
                if dot <= 1:
                    blue_stable += 1

    material_norm = (red_cells - blue_cells) / total
    mobility_norm = (len(get_valid_moves(board, PLAYER_RED)) - len(get_valid_moves(board, PLAYER_BLUE))) / total
    threat_norm = (red_threat - blue_threat) / total
    danger_norm = blue_threat / total
    stability_norm = (red_stable - blue_stable) / total
    dot_norm = (red_dots - blue_dots) / (total * 4.0)

    return material_norm, mobility_norm, threat_norm, danger_norm, stability_norm, dot_norm


def evaluate(board, dots):
    material_norm, mobility_norm, threat_norm, danger_norm, stability_norm, dot_norm = _normalized_features(
        board, dots
    )
    return (
        1.50 * material_norm
        + 0.70 * mobility_norm
        + 0.80 * threat_norm
        - 0.90 * danger_norm
        + 0.45 * stability_norm
        + 0.20 * dot_norm
    )


def _heuristic_move_score(board, dots, move, player):
    next_board, next_dots = _simulate_move(board, dots, move, player)
    score = evaluate(next_board, next_dots)
    return score if player == PLAYER_RED else -score


def _ordered_moves(board, dots, player, top_k):
    moves = get_valid_moves(board, player)
    if not moves:
        return []
    scored = [(move, _heuristic_move_score(board, dots, move, player)) for move in moves]
    scored.sort(key=lambda item: item[1], reverse=True)
    return [move for move, _ in scored[: min(top_k, len(scored))]]


def _alphabeta(board, dots, depth, alpha, beta, player, start_time, max_time):
    if time.time() - start_time >= max_time:
        raise TimeoutError

    key = _state_key(board, dots, player, depth)
    cached = _TRANSPOSITION_TABLE.get(key)
    if cached is not None:
        return cached

    moves = get_valid_moves(board, player)
    if depth == 0 or not moves:
        score = evaluate(board, dots)
        result = (score, None)
        _TRANSPOSITION_TABLE[key] = result
        return result

    next_player = PLAYER_BLUE if player == PLAYER_RED else PLAYER_RED
    ordered = _ordered_moves(board, dots, player, INNER_TOP_K)

    if player == PLAYER_RED:
        best_score = -INF
        best_move = None
        for move in ordered:
            nboard, ndots = _simulate_move(board, dots, move, player)
            score, _ = _alphabeta(nboard, ndots, depth - 1, alpha, beta, next_player, start_time, max_time)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
    else:
        best_score = INF
        best_move = None
        for move in ordered:
            nboard, ndots = _simulate_move(board, dots, move, player)
            score, _ = _alphabeta(nboard, ndots, depth - 1, alpha, beta, next_player, start_time, max_time)
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)
            if beta <= alpha:
                break

    result = (best_score, best_move)
    _TRANSPOSITION_TABLE[key] = result
    return result


def _search_root(board, dots, depth, start_time, max_time):
    root_moves = _ordered_moves(board, dots, PLAYER_RED, ROOT_TOP_K)
    if not root_moves:
        return None, []

    scored = []
    for move in root_moves:
        if time.time() - start_time >= max_time:
            raise TimeoutError
        nboard, ndots = _simulate_move(board, dots, move, PLAYER_RED)
        score, _ = _alphabeta(nboard, ndots, depth - 1, -INF, INF, PLAYER_BLUE, start_time, max_time)
        scored.append((move, score))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[0][0], scored


def _apply_noise(scored_moves):
    if len(scored_moves) < 2:
        return scored_moves[0][0] if scored_moves else None

    best_move, best_score = scored_moves[0]
    second_move, second_score = scored_moves[1]
    if abs(best_score - second_score) < NOISE_SCORE_DIFF:
        return random.choices([best_move, second_move], weights=[0.85, 0.15], k=1)[0]
    return best_move


def iterative_deepening(board, dots, max_time=MAX_THINK_TIME_SEC):
    start_time = time.time()
    _TRANSPOSITION_TABLE.clear()

    fallback_moves = get_valid_moves(board, PLAYER_RED)
    if not fallback_moves:
        return None

    best_move = fallback_moves[0]
    best_scored = [(best_move, evaluate(*_simulate_move(board, dots, best_move, PLAYER_RED)))]

    for depth in range(1, MAX_DEPTH + 1):
        try:
            move, scored = _search_root(board, dots, depth, start_time, max_time)
        except TimeoutError:
            break
        if move is None:
            break
        best_move = move
        best_scored = scored
        if time.time() - start_time >= max_time:
            break

    chosen = _apply_noise(best_scored)
    return chosen if chosen in fallback_moves else best_move


def get_hard_move(board, dots):
    return iterative_deepening(board, dots)
