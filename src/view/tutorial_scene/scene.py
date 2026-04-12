"""Tutorial scene and icon renderer."""

import pygame

from src.view.commons import make_icon_surface


def draw_tutorial_icon(screen, rect, colors, font=None):
    """Draw tutorial icon using the shared icon style."""
    icon = make_icon_surface("tutorial", rect.size, bg_color=colors["btn_amber"])
    screen.blit(icon, rect.topleft)


def _render_wrapped_lines(font, text, color, max_width):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if font.size(candidate)[0] <= max_width:
            current = candidate
            continue
        if current:
            lines.append(font.render(current, True, color))
        current = word
    if current:
        lines.append(font.render(current, True, color))
    return lines


def draw_tutorial_scene(screen, panel, fonts, colors, back_rect, tutorial_lines, back_icon):
    """Draw tutorial content scene."""
    screen.blit(back_icon, back_rect.topleft)
    title = fonts["main"].render("How to Play", True, colors["text_main"])
    subtitle = fonts["body"].render("Core mechanics, strategy, and shortcuts", True, colors["subtitle"])
    screen.blit(title, title.get_rect(center=(panel.centerx, panel.y + 84)))
    screen.blit(subtitle, subtitle.get_rect(center=(panel.centerx, panel.y + 120)))

    line_y = panel.y + 156
    text_left = panel.x + 32
    max_width = panel.width - 64
    for line in tutorial_lines:
        wrapped = _render_wrapped_lines(fonts["body"], line, colors["text_main"], max_width)
        for text in wrapped:
            screen.blit(text, (text_left, line_y))
            line_y += max(20, int(panel.height * 0.044))
        line_y += 8
