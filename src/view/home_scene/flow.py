"""Home menu scene for selecting mode and difficulty before a match."""

import pygame

from src.view.choose_diff_scene import draw_choose_diff_scene
from src.view.choose_gamemode_scene import draw_choose_gamemode_scene
from src.view.commons import make_icon_surface
from src.view.setting_scene import draw_setting_scene, draw_settings_icon
from src.view.tutorial_scene import draw_tutorial_scene

from ..window import drawScreen, toggle_fullscreen
from .assets import get_home_asset_path, load_icon_or_placeholder, load_image
from .scene import draw_home_scene

MENU = "menu"
CHOOSE_MODE = "choose_mode"
DIFFICULTY = "difficulty"
TUTORIAL = "tutorial"
SETTINGS = "settings"
MODE_PVP = "pvp"
MODE_PVBOT = "pvbot"

HOME_BG_FALLBACK = (26, 22, 24)
TITLE_COLOR = (247, 239, 224)
SUBTITLE_COLOR = (237, 228, 208)
PANEL_COLOR = (255, 248, 235)
PANEL_BORDER = (232, 215, 186)
TEXT_MAIN = (248, 240, 223)
BTN_GREEN = (92, 162, 126)
BTN_AMBER = (214, 163, 85)
BTN_RED = (194, 95, 95)
BTN_BLUE = (112, 151, 202)
BTN_SLATE = (126, 121, 110)
DIFF_COLORS = {
    "easy": (72, 137, 196),
    "medium": (236, 172, 66),
    "hard": (213, 94, 89),
}


def difficulty_from_percent(percent):
    """Map slider percentage [0..1] to difficulty."""
    value = max(0.0, min(1.0, percent))
    if value < (1.0 / 3.0):
        return "easy"
    if value < (2.0 / 3.0):
        return "medium"
    return "hard"


def _difficulty_to_percent(difficulty):
    mapping = {"easy": 0.0, "medium": 0.5, "hard": 1.0}
    return mapping.get(difficulty, 0.0)


def _draw_button(screen, rect, label, color, font):
    pygame.draw.rect(screen, color, rect, border_radius=max(12, rect.height // 4))
    pygame.draw.rect(screen, (255, 248, 235), rect, 2, border_radius=max(12, rect.height // 4))
    shadow = font.render(label, True, (30, 24, 22))
    screen.blit(shadow, shadow.get_rect(center=(rect.centerx + 1, rect.centery + 1)))
    text = font.render(label, True, (255, 248, 235))
    screen.blit(text, text.get_rect(center=rect.center))


def _draw_panel(screen, rect):
    panel_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel_surface, (255, 246, 230, 24), panel_surface.get_rect(), border_radius=24)
    pygame.draw.rect(panel_surface, (246, 224, 190, 110), panel_surface.get_rect(), 2, border_radius=24)
    screen.blit(panel_surface, rect.topleft)


def compute_menu_icon_rects(panel):
    """Return tutorial and settings icon rects for the home scene."""
    settings_icon_rect = pygame.Rect(panel.right - 58, panel.y + 16, 40, 40)
    tutorial_icon_rect = pygame.Rect(settings_icon_rect.x - 48, panel.y + 16, 40, 40)
    return tutorial_icon_rect, settings_icon_rect


def _draw_background(screen, cache):
    size = screen.get_size()
    if cache.get("source") is None:
        image_path = get_home_asset_path("background.png")
        try:
            cache["source"] = load_image(image_path, alpha=False)
        except (pygame.error, FileNotFoundError, OSError):
            cache["source"] = None

    if cache.get("size") != size:
        composed = pygame.Surface(size)
        composed.fill(HOME_BG_FALLBACK)

        source = cache.get("source")
        if source is not None:
            src_w, src_h = source.get_size()
            scale = max(size[0] / max(1, src_w), size[1] / max(1, src_h))
            target_w = max(1, int(src_w * scale))
            target_h = max(1, int(src_h * scale))
            fitted = pygame.transform.smoothscale(source, (target_w, target_h))
            pos = ((size[0] - target_w) // 2, (size[1] - target_h) // 2)
            composed.blit(fitted, pos)

        vignette = pygame.Surface(size, pygame.SRCALPHA)
        vignette.fill((5, 4, 8, 70))
        pygame.draw.rect(vignette, (255, 245, 224, 26), pygame.Rect(0, 0, size[0], int(size[1] * 0.28)))
        composed.blit(vignette, (0, 0))

        cache["image"] = composed
        cache["size"] = size

    screen.blit(cache["image"], (0, 0))


def run_home_menu():
    """Run home flow and return selected configuration or None when user exits."""
    is_fullscreen = True
    screen = drawScreen(fullscreen=is_fullscreen)
    clock = pygame.time.Clock()

    icon_size = (160, 160)
    icons = {
        "easy": load_icon_or_placeholder(get_home_asset_path("easy_icon.png"), icon_size, DIFF_COLORS["easy"]),
        "medium": load_icon_or_placeholder(get_home_asset_path("medium_icon.png"), icon_size, DIFF_COLORS["medium"]),
        "hard": load_icon_or_placeholder(get_home_asset_path("hard_icon.png"), icon_size, DIFF_COLORS["hard"]),
        "mode_pvp": load_icon_or_placeholder(get_home_asset_path("human.png"), (52, 52), BTN_BLUE),
        "mode_pvbot": load_icon_or_placeholder(get_home_asset_path("bot.png"), (52, 52), BTN_GREEN),
        "back": make_icon_surface("back", (42, 42), BTN_SLATE),
        "settings": make_icon_surface("settings", (42, 42), BTN_SLATE),
        "tutorial": make_icon_surface("tutorial", (42, 42), BTN_AMBER),
    }

    bg_cache = {}

    state = MENU
    selected_mode = MODE_PVBOT
    difficulty = "easy"
    slider_percent = _difficulty_to_percent(difficulty)
    dragging = False
    settings_return_state = MENU
    sound_enabled = True
    sound_volume = 0.75
    settings_dragging = False

    while True:
        width, height = screen.get_size()
        title_font = pygame.font.SysFont("segoeui", max(34, int(height * 0.075)), bold=True)
        main_font = pygame.font.SysFont("segoeui", max(24, int(height * 0.05)), bold=True)
        btn_font = pygame.font.SysFont("segoeui", max(20, int(height * 0.033)), bold=True)
        body_font = pygame.font.SysFont("segoeui", max(16, int(height * 0.026)))

        panel = pygame.Rect(max(24, width // 12), max(26, height // 16), width - max(48, width // 6), height - max(52, height // 10))
        back_rect = pygame.Rect(panel.x + 18, panel.y + 16, 46, 46)

        tutorial_icon_rect, settings_icon_rect = compute_menu_icon_rects(panel)

        center_x = panel.centerx
        menu_btn_w = min(340, int(panel.width * 0.56))
        menu_btn_h = max(52, int(panel.height * 0.1))
        menu_start_y = panel.y + int(panel.height * 0.46)

        play_btn = pygame.Rect(center_x - menu_btn_w // 2, menu_start_y, menu_btn_w, menu_btn_h)
        quit_btn = pygame.Rect(center_x - menu_btn_w // 2, menu_start_y + menu_btn_h + 14, menu_btn_w, menu_btn_h)

        mode_btn_h = max(46, int(panel.height * 0.085))
        mode_btn_gap = max(10, int(panel.height * 0.015))
        pvp_btn = pygame.Rect(center_x - menu_btn_w // 2, panel.y + int(panel.height * 0.45), menu_btn_w, mode_btn_h)
        pvbot_btn = pygame.Rect(center_x - menu_btn_w // 2, panel.y + int(panel.height * 0.45) + mode_btn_h + mode_btn_gap, menu_btn_w, mode_btn_h)

        slider_rect = pygame.Rect(center_x - min(180, panel.width // 3), panel.y + int(panel.height * 0.58), min(360, panel.width * 2 // 3), 22)
        knob_x = int(slider_rect.x + slider_rect.width * slider_percent)
        play_match_btn = pygame.Rect(center_x - menu_btn_w // 2, panel.bottom - menu_btn_h - 26, menu_btn_w, menu_btn_h)

        tutorial_lines = [
            "Game objective: dominate the board by creating chain explosions and converting nearby enemy cells.",
            "Turn rules: first move can only target empty cells; after that, you can play only on your own cells.",
            "Explosions: each cell bursts at 4 dots, spreads to neighbors, and can trigger long cascades.",
            "Best strategy: build pressure on edges, force opponent into low-value moves, and save detonations for combos.",
            "Shortcuts: Left Click = move, M = switch mode, R = restart match, F11 = fullscreen toggle.",
        ]

        volume_slider = pygame.Rect(panel.centerx - 160, panel.y + int(panel.height * 0.56), 290, 16)
        sound_checkbox = pygame.Rect(volume_slider.right + 14, volume_slider.centery - 12, 24, 24)
        volume_knob_x = int(volume_slider.x + volume_slider.width * sound_volume)

        palette = {
            "title": TITLE_COLOR,
            "subtitle": SUBTITLE_COLOR,
            "text_main": TEXT_MAIN,
            "btn_green": BTN_GREEN,
            "btn_amber": BTN_AMBER,
            "btn_red": BTN_RED,
            "btn_blue": BTN_BLUE,
            "btn_slate": BTN_SLATE,
            "diff_colors": DIFF_COLORS,
        }

        shared_rects = {
            "draw_button": _draw_button,
            "back_rect": back_rect,
            "play_btn": play_btn,
            "quit_btn": quit_btn,
            "pvp_btn": pvp_btn,
            "pvbot_btn": pvbot_btn,
            "slider_rect": slider_rect,
            "knob_x": knob_x,
            "play_match_btn": play_match_btn,
            "settings_icon_rect": settings_icon_rect,
            "tutorial_icon_rect": tutorial_icon_rect,
            "sound_checkbox": sound_checkbox,
            "volume_slider": volume_slider,
            "volume_knob_x": volume_knob_x,
        }

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.VIDEORESIZE and not is_fullscreen:
                screen = drawScreen(fullscreen=False, size=event.size)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    screen, is_fullscreen = toggle_fullscreen(is_fullscreen, screen)
                elif event.key == pygame.K_ESCAPE:
                    if state == MENU:
                        return None
                    if state in (CHOOSE_MODE, TUTORIAL):
                        state = MENU
                    elif state == DIFFICULTY:
                        state = CHOOSE_MODE
                    elif state == SETTINGS:
                        state = settings_return_state

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = event.pos
                if state == MENU:
                    if play_btn.collidepoint(mouse):
                        state = CHOOSE_MODE
                    elif tutorial_icon_rect.collidepoint(mouse):
                        state = TUTORIAL
                    elif settings_icon_rect.collidepoint(mouse):
                        settings_return_state = MENU
                        state = SETTINGS
                    elif quit_btn.collidepoint(mouse):
                        return None

                elif state == CHOOSE_MODE:
                    if back_rect.collidepoint(mouse):
                        state = MENU
                    elif settings_icon_rect.collidepoint(mouse):
                        settings_return_state = CHOOSE_MODE
                        state = SETTINGS
                    elif pvp_btn.collidepoint(mouse):
                        selected_mode = MODE_PVP
                        difficulty = "easy"
                        return {
                            "game_mode": selected_mode,
                            "difficulty": difficulty,
                            "audio": {"enabled": sound_enabled, "volume": sound_volume},
                        }
                    elif pvbot_btn.collidepoint(mouse):
                        selected_mode = MODE_PVBOT
                        state = DIFFICULTY

                elif state == DIFFICULTY:
                    if back_rect.collidepoint(mouse):
                        state = CHOOSE_MODE
                    elif settings_icon_rect.collidepoint(mouse):
                        settings_return_state = DIFFICULTY
                        state = SETTINGS
                    elif play_match_btn.collidepoint(mouse):
                        return {
                            "game_mode": selected_mode,
                            "difficulty": difficulty,
                            "audio": {"enabled": sound_enabled, "volume": sound_volume},
                        }
                    elif slider_rect.collidepoint(mouse):
                        dragging = True
                        slider_percent = (mouse[0] - slider_rect.x) / max(1, slider_rect.width)
                        difficulty = difficulty_from_percent(slider_percent)
                    elif abs(mouse[0] - knob_x) <= 24 and abs(mouse[1] - slider_rect.centery) <= 24:
                        dragging = True

                elif state == TUTORIAL:
                    if back_rect.collidepoint(mouse):
                        state = MENU
                    elif settings_icon_rect.collidepoint(mouse):
                        settings_return_state = TUTORIAL
                        state = SETTINGS

                elif state == SETTINGS:
                    if back_rect.collidepoint(mouse):
                        state = settings_return_state
                    elif sound_checkbox.collidepoint(mouse):
                        sound_enabled = not sound_enabled
                    elif volume_slider.collidepoint(mouse):
                        settings_dragging = True
                        sound_volume = (mouse[0] - volume_slider.x) / max(1, volume_slider.width)
                    elif abs(mouse[0] - volume_knob_x) <= 20 and abs(mouse[1] - volume_slider.centery) <= 20:
                        settings_dragging = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False
                settings_dragging = False

            if event.type == pygame.MOUSEMOTION and dragging and state == DIFFICULTY:
                slider_percent = (event.pos[0] - slider_rect.x) / max(1, slider_rect.width)
                difficulty = difficulty_from_percent(slider_percent)

            if event.type == pygame.MOUSEMOTION and settings_dragging and state == SETTINGS:
                sound_volume = (event.pos[0] - volume_slider.x) / max(1, volume_slider.width)

        slider_percent = max(0.0, min(1.0, slider_percent))
        sound_volume = max(0.0, min(1.0, sound_volume))
        if not dragging:
            slider_percent = _difficulty_to_percent(difficulty)

        _draw_background(screen, bg_cache)
        _draw_panel(screen, panel)

        if state == MENU:
            draw_home_scene(
                screen,
                panel,
                {"title": title_font, "body": body_font, "button": btn_font},
                palette,
                shared_rects,
            )
            draw_settings_icon(screen, settings_icon_rect, palette)
            screen.blit(icons["tutorial"], tutorial_icon_rect.topleft)

        elif state == CHOOSE_MODE:
            draw_choose_gamemode_scene(
                screen,
                panel,
                {"main": main_font, "button": btn_font},
                palette,
                shared_rects,
                icons,
            )

        elif state == DIFFICULTY:
            shared_rects["knob_x"] = int(slider_rect.x + slider_rect.width * slider_percent)
            draw_choose_diff_scene(
                screen,
                panel,
                {"main": main_font, "body": body_font, "button": btn_font},
                palette,
                shared_rects,
                difficulty,
                icons,
            )

        elif state == TUTORIAL:
            draw_settings_icon(screen, settings_icon_rect, palette)
            draw_tutorial_scene(
                screen,
                panel,
                {"main": main_font, "body": body_font},
                palette,
                back_rect,
                tutorial_lines,
                icons["back"],
            )
        else:
            draw_setting_scene(
                screen,
                panel,
                {"main": main_font, "body": body_font},
                palette,
                back_rect,
                icons["back"],
                {
                    "sound_checkbox": sound_checkbox,
                    "volume_slider": volume_slider,
                    "volume_knob_x": int(volume_slider.x + volume_slider.width * sound_volume),
                    "sound_enabled": sound_enabled,
                    "sound_volume": sound_volume,
                },
            )

        pygame.display.flip()
        clock.tick(60)
