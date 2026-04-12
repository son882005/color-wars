"""Setting scene and icon renderer."""

import pygame

from src.view.commons import make_icon_surface


def draw_settings_icon(screen, rect, colors):
    """Draw settings icon using the shared icon style."""
    icon = make_icon_surface("settings", rect.size, bg_color=colors["btn_slate"])
    screen.blit(icon, rect.topleft)


def draw_setting_scene(screen, panel, fonts, colors, back_rect, back_icon, controls):
    """Draw settings scene content."""
    screen.blit(back_icon, back_rect.topleft)
    title = fonts["main"].render("Settings", True, colors["text_main"])
    subtitle = fonts["body"].render("Audio, display, and match preferences", True, colors["subtitle"])
    hint = fonts["body"].render("Music control is live, future toggles can be added here.", True, colors["text_main"])

    screen.blit(title, title.get_rect(center=(panel.centerx, panel.y + 84)))
    screen.blit(subtitle, subtitle.get_rect(center=(panel.centerx, panel.y + 150)))
    screen.blit(hint, hint.get_rect(center=(panel.centerx, panel.y + 184)))

    checkbox_rect = controls["sound_checkbox"]
    slider_rect = controls["volume_slider"]
    knob_x = controls["volume_knob_x"]
    sound_enabled = controls["sound_enabled"]
    sound_volume = controls["sound_volume"]

    pygame.draw.rect(screen, (238, 244, 248), checkbox_rect, border_radius=5)
    pygame.draw.rect(screen, colors["btn_slate"], checkbox_rect, 2, border_radius=5)
    if sound_enabled:
        tick_points = [
            (checkbox_rect.x + 5, checkbox_rect.centery),
            (checkbox_rect.x + 10, checkbox_rect.bottom - 6),
            (checkbox_rect.right - 5, checkbox_rect.y + 6),
        ]
        pygame.draw.lines(screen, colors["btn_green"], False, tick_points, 3)

    volume_label = fonts["body"].render(f"Volume {int(sound_volume * 100)}%", True, colors["text_main"])
    screen.blit(volume_label, (slider_rect.x, slider_rect.y - 30))

    pygame.draw.rect(screen, (216, 224, 230), slider_rect, border_radius=8)
    fill_w = max(1, knob_x - slider_rect.x)
    fill_rect = pygame.Rect(slider_rect.x, slider_rect.y, fill_w, slider_rect.height)
    pygame.draw.rect(screen, colors["btn_blue"], fill_rect, border_radius=8)
    pygame.draw.circle(screen, (255, 255, 255), (knob_x, slider_rect.centery), 12)
    pygame.draw.circle(screen, colors["btn_blue"], (knob_x, slider_rect.centery), 9)
