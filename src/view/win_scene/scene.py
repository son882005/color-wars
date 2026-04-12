"""Win scene overlay renderer."""

import pygame

from src.engine.rules import PLAYER_BLUE


def get_win_action_rects(screen):
    """Compute clickable controls for the end screen."""
    width, height = screen.get_size()
    panel_w = min(680, int(width * 0.68))
    panel_h = min(440, int(height * 0.62))
    panel = pygame.Rect((width - panel_w) // 2, (height - panel_h) // 2, panel_w, panel_h)

    restart_rect = pygame.Rect(0, 0, 72, 72)
    restart_rect.center = (panel.centerx, panel.y + int(panel_h * 0.55))

    home_rect = pygame.Rect(0, 0, 220, 58)
    home_rect.center = (panel.centerx, panel.bottom - 72)

    return {
        "panel": panel,
        "restart_rect": restart_rect,
        "home_rect": home_rect,
    }


def draw_win_scene(screen, winner, icons):
    """Draw full-screen win scene and return action rects."""
    if winner is None:
        return {}

    rects = get_win_action_rects(screen)
    panel = rects["panel"]
    restart_rect = rects["restart_rect"]
    home_rect = rects["home_rect"]

    shade = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    shade.fill((7, 12, 21, 150))
    screen.blit(shade, (0, 0))

    pygame.draw.rect(screen, (246, 250, 253), panel, border_radius=26)

    accent = (46, 125, 193) if winner == PLAYER_BLUE else (206, 79, 79)
    pygame.draw.rect(screen, accent, panel, 4, border_radius=26)

    title_font = pygame.font.SysFont("segoeui", max(34, int(panel.height * 0.1)), bold=True)
    body_font = pygame.font.SysFont("segoeui", max(18, int(panel.height * 0.06)), bold=True)
    button_font = pygame.font.SysFont("segoeui", 26, bold=True)

    winner_name = "BLUE PLAYER" if winner == PLAYER_BLUE else "RED PLAYER"
    title = title_font.render("MATCH ENDED", True, (32, 45, 56))
    winner_text = body_font.render(f"Winner: {winner_name}", True, accent)
    subtitle = body_font.render("Choose what to do next", True, (68, 84, 98))

    screen.blit(title, title.get_rect(center=(panel.centerx, panel.y + 88)))
    screen.blit(winner_text, winner_text.get_rect(center=(panel.centerx, panel.y + 150)))
    screen.blit(subtitle, subtitle.get_rect(center=(panel.centerx, panel.y + 190)))

    screen.blit(icons["restart"], restart_rect.topleft)

    pygame.draw.rect(screen, accent, home_rect, border_radius=16)
    home_label = button_font.render("HOME", True, (255, 255, 255))
    screen.blit(home_label, home_label.get_rect(center=home_rect.center))

    return rects
