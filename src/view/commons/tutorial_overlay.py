"""Reusable tutorial overlay that can be drawn on top of any scene."""

import pygame


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


def draw_tutorial_overlay(screen, panel, fonts, colors, lines, close_label="Dong"):
    """Draw translucent overlay with beginner tutorial content.

    Returns:
        dict containing close button rect.
    """
    shade = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    shade.fill((8, 16, 26, 150))
    screen.blit(shade, (0, 0))

    overlay_w = min(int(panel.width * 0.9), screen.get_width() - 32)
    overlay_h = min(int(panel.height * 0.88), screen.get_height() - 32)
    overlay = pygame.Rect(
        (screen.get_width() - overlay_w) // 2,
        (screen.get_height() - overlay_h) // 2,
        overlay_w,
        overlay_h,
    )

    pygame.draw.rect(screen, (248, 243, 232), overlay, border_radius=18)
    pygame.draw.rect(screen, colors["btn_slate"], overlay, 3, border_radius=18)

    title = fonts["main"].render("Huong dan nhanh", True, colors["text_main"])
    subtitle = fonts["body"].render("Meo co ban cho nguoi moi", True, colors["subtitle"])
    screen.blit(title, title.get_rect(center=(overlay.centerx, overlay.y + 48)))
    screen.blit(subtitle, subtitle.get_rect(center=(overlay.centerx, overlay.y + 84)))

    text_left = overlay.x + 22
    text_max_width = overlay.width - 44
    line_y = overlay.y + 120
    step_idx = 1
    for line in lines:
        wrapped = _render_wrapped_lines(fonts["body"], f"{step_idx}. {line}", colors["text_main"], text_max_width)
        for text in wrapped:
            if line_y + text.get_height() > overlay.bottom - 64:
                break
            screen.blit(text, (text_left, line_y))
            line_y += max(19, int(overlay.height * 0.052))
        line_y += 4
        step_idx += 1
        if line_y > overlay.bottom - 64:
            break

    close_rect = pygame.Rect(overlay.right - 128, overlay.bottom - 48, 96, 32)
    pygame.draw.rect(screen, colors["btn_blue"], close_rect, border_radius=8)
    label = fonts["body"].render(close_label, True, (255, 255, 255))
    screen.blit(label, label.get_rect(center=close_rect.center))

    return {"overlay": overlay, "close_rect": close_rect}
