"""Main runtime loop: input, AI turn, and render."""

import pygame

from src.ai import get_ai_move
from src.controller import apply_move, get_scores
from src.engine.rules import PLAYER_BLUE, PLAYER_RED
from src.game.state import GameState
from src import view
from src.game.audio import set_music_enabled, update_music_volume
from src.view.commons import make_icon_surface

MODE_PVP = "pvp"
MODE_PVBOT = "pvbot"
FPS = 60
EXPLOSION_ANIMATION_MS = 140


def run_game(game_mode=MODE_PVBOT, difficulty="easy", audio=None):
    """Run one match in pvp or pvbot mode."""
    if game_mode not in (MODE_PVP, MODE_PVBOT):
        game_mode = MODE_PVBOT
    if difficulty not in ("easy", "medium", "hard", "ez", "med"):
        difficulty = "easy"
    if difficulty == "ez":
        difficulty = "easy"
    if difficulty == "med":
        difficulty = "medium"

    audio = audio or {}

    state = GameState()

    is_fullscreen = True
    screen = view.drawScreen(fullscreen=is_fullscreen)
    clock = pygame.time.Clock()
    sound_enabled = bool(audio.get("enabled", True))
    sound_volume = float(audio.get("volume", 0.75))
    ui_icons = {
        "back": make_icon_surface("back", (40, 40), bg_color=(89, 114, 135)),
        "settings": make_icon_surface("settings", (40, 40), bg_color=(89, 114, 135)),
        "restart": make_icon_surface("restart", (72, 72), bg_color=(89, 114, 135)),
    }
    settings_open = False
    set_music_enabled(sound_enabled, sound_volume)
    settings_dragging = False

    running = True

    def get_corner_rects():
        width, _ = screen.get_size()
        return {
            "back": pygame.Rect(12, 10, 40, 40),
            "settings": pygame.Rect(width - 52, 10, 40, 40),
        }

    def get_settings_rects():
        width, height = screen.get_size()
        panel = pygame.Rect((width - 380) // 2, (height - 240) // 2, 380, 240)
        slider = pygame.Rect(panel.x + 34, panel.y + 162, panel.width - 112, 16)
        checkbox = pygame.Rect(slider.right + 14, slider.centery - 12, 24, 24)
        knob_x = int(slider.x + slider.width * sound_volume)
        return {
            "panel": panel,
            "checkbox": checkbox,
            "slider": slider,
            "knob_x": knob_x,
        }

    def draw_corner_icons():
        rects = get_corner_rects()
        screen.blit(ui_icons["back"], rects["back"].topleft)
        screen.blit(ui_icons["settings"], rects["settings"].topleft)

    def draw_settings_overlay():
        rects = get_settings_rects()
        panel = rects["panel"]
        checkbox = rects["checkbox"]
        slider = rects["slider"]
        knob_x = rects["knob_x"]

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((8, 16, 26, 110))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (244, 248, 252), panel, border_radius=18)
        pygame.draw.rect(screen, (86, 111, 132), panel, 3, border_radius=18)

        title_font = pygame.font.SysFont("segoeui", 30, bold=True)
        body_font = pygame.font.SysFont("segoeui", 23, bold=False)
        title = title_font.render("Gameplay Settings", True, (35, 52, 66))
        screen.blit(title, (panel.x + 30, panel.y + 28))

        pygame.draw.rect(screen, (238, 244, 248), checkbox, border_radius=5)
        pygame.draw.rect(screen, (86, 111, 132), checkbox, 2, border_radius=5)
        if sound_enabled:
            points = [
                (checkbox.x + 5, checkbox.centery),
                (checkbox.x + 10, checkbox.bottom - 6),
                (checkbox.right - 5, checkbox.y + 6),
            ]
            pygame.draw.lines(screen, (75, 165, 98), False, points, 3)

        volume_text = body_font.render(f"Volume {int(sound_volume * 100)}%", True, (35, 52, 66))
        screen.blit(volume_text, (slider.x, slider.y - 34))
        pygame.draw.rect(screen, (212, 223, 232), slider, border_radius=8)
        fill_rect = pygame.Rect(slider.x, slider.y, max(1, knob_x - slider.x), slider.height)
        pygame.draw.rect(screen, (72, 137, 196), fill_rect, border_radius=8)
        pygame.draw.circle(screen, (255, 255, 255), (knob_x, slider.centery), 11)
        pygame.draw.circle(screen, (72, 137, 196), (knob_x, slider.centery), 8)

        return rects

    def play_explosion_animation(steps):
        nonlocal running, screen, is_fullscreen
        if not steps:
            return

        frames_per_step = max(4, int(FPS * EXPLOSION_ANIMATION_MS / 1000))
        for step in steps:
            for frame in range(frames_per_step):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        return
                    if event.type == pygame.VIDEORESIZE and not is_fullscreen:
                        screen = view.drawScreen(fullscreen=False, size=event.size)
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                        screen, is_fullscreen = view.toggle_fullscreen(is_fullscreen, screen)

                if not running:
                    return

                blue_score, red_score = get_scores(state)
                view.drawScene(
                    screen,
                    state,
                    state.board,
                    state.dots,
                    state.current_player,
                    blue_score,
                    red_score,
                    state.winner,
                    game_mode,
                    difficulty,
                )
                progress = (frame + 1) / frames_per_step
                layout = view.compute_layout(screen, state.grid_size)
                view.drawExplosionOverlay(screen, layout, step, progress)
                pygame.display.flip()
                clock.tick(FPS)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE and not is_fullscreen:
                screen = view.drawScreen(fullscreen=False, size=event.size)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    state = GameState()
                elif event.key == pygame.K_m:
                    game_mode = MODE_PVP if game_mode == MODE_PVBOT else MODE_PVBOT
                    state = GameState()
                elif event.key == pygame.K_F11:
                    screen, is_fullscreen = view.toggle_fullscreen(is_fullscreen, screen)
                elif event.key == pygame.K_ESCAPE:
                    if state.winner is None and settings_open:
                        settings_open = False
                    else:
                        return "home"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = event.pos
                corner_rects = get_corner_rects()

                if state.winner is not None:
                    win_rects = view.get_win_action_rects(screen)
                    if win_rects["restart_rect"].collidepoint(mouse):
                        state = GameState()
                        settings_open = False
                    elif win_rects["home_rect"].collidepoint(mouse):
                        return "home"
                    continue

                if corner_rects["back"].collidepoint(mouse):
                    return "home"
                if corner_rects["settings"].collidepoint(mouse):
                    settings_open = not settings_open
                    continue

                if settings_open:
                    rects = get_settings_rects()
                    checkbox = rects["checkbox"]
                    slider = rects["slider"]
                    knob_x = rects["knob_x"]
                    if checkbox.collidepoint(mouse):
                        sound_enabled = not sound_enabled
                        set_music_enabled(sound_enabled, sound_volume)
                    elif slider.collidepoint(mouse):
                        settings_dragging = True
                        sound_volume = (mouse[0] - slider.x) / max(1, slider.width)
                        update_music_volume(sound_volume)
                    elif abs(mouse[0] - knob_x) <= 18 and abs(mouse[1] - slider.centery) <= 18:
                        settings_dragging = True
                    continue

                if game_mode == MODE_PVP or state.current_player == PLAYER_BLUE:
                    row, col = view.get_cell_from_mouse(mouse, state.grid_size, screen)
                    explosion_steps = []
                    moved = apply_move(
                        state,
                        row,
                        col,
                        explosion_callback=explosion_steps.append,
                    )
                    if moved:
                        play_explosion_animation(explosion_steps)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                settings_dragging = False
            elif event.type == pygame.MOUSEMOTION and settings_dragging and settings_open:
                slider = get_settings_rects()["slider"]
                sound_volume = (event.pos[0] - slider.x) / max(1, slider.width)
                update_music_volume(sound_volume)

        if game_mode == MODE_PVBOT and state.winner is None and state.current_player == PLAYER_RED:
            move = get_ai_move(state.board, state.dots, difficulty)

            if move is None:
                blue_score, red_score = get_scores(state)
                if red_score == 0 and blue_score > 0:
                    state.winner = PLAYER_BLUE
                elif blue_score == 0 and red_score > 0:
                    state.winner = PLAYER_RED
                else:
                    state.current_player = PLAYER_BLUE
            else:
                explosion_steps = []
                moved = apply_move(
                    state,
                    move[0],
                    move[1],
                    player=PLAYER_RED,
                    explosion_callback=explosion_steps.append,
                )
                if moved:
                    play_explosion_animation(explosion_steps)

        blue_score, red_score = get_scores(state)
        view.drawScene(
            screen,
            state,
            state.board,
            state.dots,
            state.current_player,
            blue_score,
            red_score,
            state.winner,
            game_mode,
            difficulty,
        )

        draw_corner_icons()
        if settings_open and state.winner is None:
            draw_settings_overlay()

        if state.winner is not None:
            view.draw_win_scene(screen, state.winner, ui_icons)

        pygame.display.flip()
        clock.tick(FPS)

    return None
