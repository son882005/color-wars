"""Main Ứng dụng game Color Wars."""

import pygame
import sys

if __package__ is None or __package__ == "":
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.game.loop import run_game
from src.game.audio import get_music_manager
from src.game.settings import AppSettings
from src.view.home_scene import run_home_menu


def main():
    """Khởi chạy game ở mode mặc định"""

    # Khởi tạo toàn bộ subsystem của pygame trước khi render/game loop.
    pygame.init()
    settings = AppSettings()
    music = get_music_manager()
    try:
        while True:
            music.start_new_menu_session()
            music.enter_menu()
            launch_config = run_home_menu(settings=settings, music=music)
            if launch_config is None:
                break

            result = run_game(
                game_mode=launch_config.get("game_mode", "pvbot"),
                difficulty=launch_config.get("difficulty", "easy"),
                settings=settings,
                music=music,
            )
            if result is None:
                break
    finally:
        # Giải phóng tài nguyên pygame ngay cả khi có exception ở menu hoặc gameplay.
        pygame.quit()

if __name__ == "__main__":
    main()