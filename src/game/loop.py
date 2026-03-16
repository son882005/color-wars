import pygame

from src.ai import get_ai_move
from src.controller import apply_move, get_scores
from src.engine.rules import PLAYER_BLUE, PLAYER_RED
from src.game.state import GameState
from src import view

MODE_PVP = "pvp"
MODE_PVBOT = "pvbot"
FPS = 60


def run_game(game_mode=MODE_PVBOT):
    if game_mode not in (MODE_PVP, MODE_PVBOT):
        game_mode = MODE_PVBOT

    state = GameState()

    screen = view.drawScreen()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_mode == MODE_PVP or state.current_player == PLAYER_BLUE:
                    row, col = view.get_cell_from_mouse(event.pos, state.grid_size)
                    apply_move(state, row, col)

        if game_mode == MODE_PVBOT and state.winner is None and state.current_player == PLAYER_RED:
            move = get_ai_move(state.board, state.dots)

            if move is None:
                blue_score, red_score = get_scores(state)
                if red_score == 0 and blue_score > 0:
                    state.winner = PLAYER_BLUE
                elif blue_score == 0 and red_score > 0:
                    state.winner = PLAYER_RED
                else:
                    state.current_player = PLAYER_BLUE
            else:
                apply_move(state, move[0], move[1], player=PLAYER_RED)

        blue_score, red_score = get_scores(state)
        view.drawScene(screen, state.board, state.dots, state.current_player, blue_score, red_score, state.winner)

        pygame.display.flip()
        clock.tick(FPS)
