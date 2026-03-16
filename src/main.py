import pygame
import sys
import argparse

if __package__ is None or __package__ == "":
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.game.loop import run_game


def main():
    parser = argparse.ArgumentParser(description="Color Wars")
    parser.add_argument(
        "--mode",
        choices=["pvp", "pvbot"],
        default="pvbot",
        help="Game mode: pvp (2 players) or pvbot (player vs bot)",
    )
    args = parser.parse_args()

    pygame.init()
    run_game(args.mode)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()