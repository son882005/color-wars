from src.engine.explosion import resolve_explosions
from src.engine.rules import PLAYER_BLUE, PLAYER_RED, get_move_dot_increment, get_valid_moves


def get_scores(state):
    blue_cells = 0
    red_cells = 0
    for row in range(state.grid_size):
        for col in range(state.grid_size):
            if state.board[row][col] == PLAYER_BLUE:
                blue_cells += 1
            elif state.board[row][col] == PLAYER_RED:
                red_cells += 1
    return blue_cells, red_cells


def update_winner(state):
    blue_cells, red_cells = get_scores(state)
    total_cells = state.grid_size * state.grid_size

    if blue_cells > 0:
        state.blue_has_initialized = True
    if red_cells > 0:
        state.red_has_initialized = True

    if blue_cells == total_cells:
        state.winner = PLAYER_BLUE
    elif red_cells == total_cells:
        state.winner = PLAYER_RED
    elif state.red_has_initialized and red_cells == 0 and blue_cells > 0:
        state.winner = PLAYER_BLUE
    elif state.blue_has_initialized and blue_cells == 0 and red_cells > 0:
        state.winner = PLAYER_RED


def apply_move(state, row, col, player=None):
    if state.winner is not None:
        return False

    if row is None or col is None:
        return False

    active_player = state.current_player if player is None else player
    valid_moves = get_valid_moves(state.board, active_player)
    if (row, col) not in valid_moves:
        return False

    increment = get_move_dot_increment(state.board, row, col)
    state.board[row][col] = active_player
    state.dots[row][col] += increment

    resolve_explosions(state.board, state.dots, row, col)

    state.turn_count += 1
    update_winner(state)

    if state.winner is None:
        state.current_player = PLAYER_RED if active_player == PLAYER_BLUE else PLAYER_BLUE

    return True