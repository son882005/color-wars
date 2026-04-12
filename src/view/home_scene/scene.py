"""Home scene renderer."""


def _blit_shadow_text(screen, font, text, color, center, shadow_color=(10, 14, 22), offset=(2, 2)):
    """Draw text with subtle shadow to keep readability on busy backgrounds."""
    shadow = font.render(text, True, shadow_color)
    screen.blit(shadow, shadow.get_rect(center=(center[0] + offset[0], center[1] + offset[1])))
    main = font.render(text, True, color)
    screen.blit(main, main.get_rect(center=center))


def draw_home_scene(screen, panel, fonts, colors, rects):
    """Draw the main home scene."""
    center_x = panel.centerx
    _blit_shadow_text(screen, fonts["title"], "COLOR WARS", colors["title"], (center_x, panel.y + 88))
    _blit_shadow_text(
        screen,
        fonts["body"],
        "Dễ làm quen, khó tinh thông",
        colors["subtitle"],
        (center_x, panel.y + 138),
        shadow_color=(10, 14, 22),
        offset=(1, 1),
    )

    draw_button = rects["draw_button"]
    draw_button(screen, rects["play_btn"], "PLAY", colors["btn_green"], fonts["button"])
    draw_button(screen, rects["quit_btn"], "QUIT", colors["btn_red"], fonts["button"])
