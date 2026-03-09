import pygame

HEIGHT = 600
WIDTH = 800

BOARD_SIZE = 500  # 5 nodes x 100px
NODE_SIZE = 100
BORDER_WIDTH = 1

BG_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE_COLOR = (90, 188, 236)
RED_COLOR = (235, 112, 102)

def drawScreen():
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    SCREEN.fill(BG_COLOR)
    pygame.display.set_caption("Color Wars")
    return SCREEN

def drawBoard(SCREEN, BOARD, DOTS):
    start_x = (WIDTH - BOARD_SIZE) // 2
    start_y = (HEIGHT - BOARD_SIZE) // 2

    for i in range(5):
        for j in range(5):

            x = start_x + i * NODE_SIZE
            y = start_y + j * NODE_SIZE

            rect = (x, y, NODE_SIZE, NODE_SIZE)
            drawNode(SCREEN, rect)

            if BOARD[j][i] == 1:
                drawDot(SCREEN, x, y, 1, BLUE_COLOR)

            if DOTS[j][i] > 0:
                color = BLUE_COLOR if BOARD[j][i] == 1 else RED_COLOR
                drawDot(SCREEN, x, y, DOTS[j][i], color)

def drawNode(SCREEN, game):
    pygame.draw.rect(SCREEN, WHITE, game, BORDER_WIDTH)

def drawDot(SCREEN, x, y, count, color):
    cx = x + NODE_SIZE//2
    cy = y + NODE_SIZE//2

    if count == 1:
        pygame.draw.circle(SCREEN, color, (cx, cy), 10)

    elif count == 2:
        pygame.draw.circle(SCREEN, color, (cx-15, cy), 10)
        pygame.draw.circle(SCREEN, color, (cx+15, cy), 10)

    elif count == 3:
        pygame.draw.circle(SCREEN, color, (cx-15, cy), 10)
        pygame.draw.circle(SCREEN, color, (cx+15, cy), 10)
        pygame.draw.circle(SCREEN, color, (cx, cy-15), 10)