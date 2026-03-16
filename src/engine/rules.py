EMPTY = 0
PLAYER_BLUE = 1
PLAYER_RED = 2


def in_bounds(row, col, size):
    return 0 <= row < size and 0 <= col < size


def get_capacity(row, col, size):
    return 4


def get_valid_moves(board, player):
    size = len(board)
    own_cells = []
    empty_cells = []

    for row in range(size):
        for col in range(size):
            if board[row][col] == player:
                own_cells.append((row, col))
            elif board[row][col] == EMPTY:
                empty_cells.append((row, col))

    if own_cells:
        return own_cells

    return empty_cells


def get_move_dot_increment(board, row, col):
    if board[row][col] == EMPTY:
        return 3

    return 1
