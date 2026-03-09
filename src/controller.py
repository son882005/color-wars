import pygame
import view

BOARD_SIZE = 5  # Kích thước lưới (5x5)
EXPLODE_DOTS = 4  # Số dot để ô nổ
PLAYER_BLUE = 1  # Giá trị đại diện cho người chơi xanh
PLAYER_RED = 2   # Giá trị đại diện cho người chơi đỏ

# Trạng thái board: BOARD lưu chủ sở hữu ô, DOTS lưu số dot trong ô
BOARD = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
DOTS  = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Người chơi hiện tại
current_player = PLAYER_BLUE

def explode(row, col):

    # Nếu số dot chưa đủ để nổ thì thoát
    if DOTS[row][col] < EXPLODE_DOTS:
        return

    player = BOARD[row][col]

    # Xóa hết dot và chủ sở hữu ô vừa nổ
    DOTS[row][col] = 0
    BOARD[row][col] = 0

    # Đánh dấu ô vừa nổ để không nhận dot lại trong chuỗi nổ
    exploded_cells = set()
    exploded_cells.add((row, col))

    # 4 hướng lân cận
    directions = [
        (-1,0),
        (1,0),
        (0,-1),
        (0,1)
    ]

    for dr, dc in directions:
        r = row + dr
        c = col + dc
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            # Không phân dot về ô vừa nổ
            if (r, c) in exploded_cells:
                continue
            # Ô trống: đồng hóa và cộng 1 dot
            if BOARD[r][c] == 0:
                BOARD[r][c] = player
                DOTS[r][c] += 1
            # Ô đồng minh: chỉ cộng 1 dot
            elif BOARD[r][c] == player:
                DOTS[r][c] += 1
            # Ô địch: đồng hóa và cộng 1 dot
            else:
                BOARD[r][c] = player
                DOTS[r][c] += 1
            # Kiểm tra tiếp nếu ô vừa nhận dot đủ để nổ
            explode(r, c)

def handleClick(pos):
    global current_player

    start_x = (view.WIDTH - view.BOARD_SIZE) // 2
    start_y = (view.HEIGHT - view.BOARD_SIZE) // 2

    x, y = pos

    # Xác định vị trí ô được click
    col = (x - start_x) // view.NODE_SIZE
    row = (y - start_y) // view.NODE_SIZE

    # Chỉ xử lý nếu click trong board
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        # Chỉ cho phép đặt dot vào ô trống hoặc ô của mình
        if BOARD[row][col] in (0, current_player):
            BOARD[row][col] = current_player
            DOTS[row][col] += 1
            # Kiểm tra nổ
            explode(row, col)
            # Chuyển lượt cho người chơi tiếp theo
            current_player = PLAYER_RED if current_player == PLAYER_BLUE else PLAYER_BLUE

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