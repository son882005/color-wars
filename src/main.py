"""Main Ứng dụng game Color Wars."""

import pygame
import sys

if __package__ is None or __package__ == "":
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.game.loop import run_game


def main():
    """Khởi chạy game ở mode mặc định"""

    # Khởi tạo toàn bộ subsystem của pygame trước khi render/game loop.
    pygame.init()
    run_game()
    # Giải phóng tài nguyên pygame trước khi thoát tiến trình.
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()