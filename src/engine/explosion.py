from collections import deque

from .rules import EMPTY, get_capacity, in_bounds

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def resolve_explosions(board, dots, start_row, start_col):
    size = len(board)
    queue = deque([(start_row, start_col)])

    while queue:
        row, col = queue.popleft()
        owner = board[row][col]

        if owner == EMPTY:
            continue

        if dots[row][col] < get_capacity(row, col, size):
            continue

        dots[row][col] = 0
        board[row][col] = EMPTY

        for dr, dc in DIRECTIONS:
            nr, nc = row + dr, col + dc
            if not in_bounds(nr, nc, size):
                continue

            board[nr][nc] = owner
            dots[nr][nc] += 1

            if dots[nr][nc] >= get_capacity(nr, nc, size):
                queue.append((nr, nc))
