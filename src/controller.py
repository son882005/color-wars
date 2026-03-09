import pygame
import view

BOARD = [[0 for _ in range(5)] for _ in range(5)]
DOTS  = [[0 for _ in range(5)] for _ in range(5)]

current_player = 1

def explode(row, col):

    if DOTS[row][col] < 4:
        return

    player = BOARD[row][col]

    DOTS[row][col] = 0
    BOARD[row][col] = 0

    directions = [
        (-1,0),
        (1,0),
        (0,-1),
        (0,1)
    ]

    for dr, dc in directions:
        r = row + dr
        c = col + dc
        if 0 <= r < 5 and 0 <= c < 5:
            if BOARD[r][c] == 0:
                BOARD[r][c] = player
                DOTS[r][c] += 1
            elif BOARD[r][c] == player:
                DOTS[r][c] += 1
            else:
                BOARD[r][c] = player
                DOTS[r][c] += 1
            explode(r, c)

def handleClick(pos):
    global current_player

    start_x = (view.WIDTH - view.BOARD_SIZE) // 2
    start_y = (view.HEIGHT - view.BOARD_SIZE) // 2

    x, y = pos

    col = (x - start_x) // view.NODE_SIZE
    row = (y - start_y) // view.NODE_SIZE

    if 0 <= row < 5 and 0 <= col < 5:

        if BOARD[row][col] in (0, current_player):

            BOARD[row][col] = current_player
            DOTS[row][col] += 1

            explode(row, col)

            current_player = 2 if current_player == 1 else 1

def runGame():
    SCREEN = view.drawScreen()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                handleClick(event.pos)

        view.drawBoard(SCREEN, BOARD, DOTS)
        
        pygame.display.flip()