import pygame

HEIGHT = 600
WIDTH = 800

BOARD_SIZE = 500
NODE_SIZE = 100
BORDER_WIDTH = 1

BG_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE_COLOR = (90, 188, 236)
RED_COLOR = (235, 112, 102)
HUD_TEXT_COLOR = (230, 230, 230)

EMPTY = 0
PLAYER_BLUE = 1
PLAYER_RED = 2

def get_board_origin():
    start_x = (WIDTH - BOARD_SIZE) // 2
    start_y = (HEIGHT - BOARD_SIZE) // 2
    return start_x, start_y

def get_cell_from_mouse(mouse_pos, grid_size):
    start_x, start_y = get_board_origin()
    x, y = mouse_pos

    local_x = x - start_x
    local_y = y - start_y

    if local_x < 0 or local_y < 0:
        return None, None
    if local_x >= BOARD_SIZE or local_y >= BOARD_SIZE:
        return None, None

    col = local_x // NODE_SIZE
    row = local_y // NODE_SIZE

    if 0 <= row < grid_size and 0 <= col < grid_size:
        return row, col
    return None, None

def drawScreen():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Color Wars")
    return screen


def drawScene(screen, board, dots, current_player, blue_score, red_score, winner):
    screen.fill(BG_COLOR)
    drawBoard(screen, board, dots)
    drawHud(screen, current_player, blue_score, red_score, winner)


def drawBoard(screen, board, dots):
    start_x, start_y = get_board_origin()
    grid_size = len(board)

    for row in range(grid_size):
        for col in range(grid_size):
            x = start_x + col * NODE_SIZE
            y = start_y + row * NODE_SIZE
            rect = (x, y, NODE_SIZE, NODE_SIZE)
            drawNode(screen, rect)

            if board[row][col] == EMPTY or dots[row][col] <= 0:
                continue

            color = BLUE_COLOR if board[row][col] == PLAYER_BLUE else RED_COLOR
            drawDot(screen, x, y, dots[row][col], color)


def drawNode(screen, rect):
    pygame.draw.rect(screen, WHITE, rect, BORDER_WIDTH)


def drawDot(screen, x, y, count, color):
    cx = x + NODE_SIZE // 2
    cy = y + NODE_SIZE // 2
    radius = 10
    gap = 15

    if count == 1:
        positions = [(cx, cy)]
    elif count == 2:
        positions = [(cx - gap, cy), (cx + gap, cy)]
    elif count == 3:
        positions = [(cx - gap, cy), (cx + gap, cy), (cx, cy - gap)]
    else:
        # Fallback để render ổn nếu có count lớn hơn thiết kế.
        positions = [
            (cx - gap, cy - gap),
            (cx + gap, cy - gap),
            (cx - gap, cy + gap),
            (cx + gap, cy + gap),
        ]

    for px, py in positions:
        pygame.draw.circle(screen, color, (px, py), radius)


def drawHud(screen, current_player, blue_score, red_score, winner):
    font = pygame.font.SysFont("consolas", 24)

    score_text = f"Blue: {blue_score}   Red: {red_score}"
    if winner is None:
        turn_name = "Blue" if current_player == PLAYER_BLUE else "Red"
        status_text = f"Turn: {turn_name}"
    else:
        winner_name = "Blue" if winner == PLAYER_BLUE else "Red"
        status_text = f"Winner: {winner_name}"

    score_surface = font.render(score_text, True, HUD_TEXT_COLOR)
    status_surface = font.render(status_text, True, HUD_TEXT_COLOR)

    screen.blit(score_surface, (20, 16))
    screen.blit(status_surface, (20, 46))