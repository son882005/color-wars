"""Choose game mode scene renderer."""

import pygame


def draw_choose_gamemode_scene(screen, panel, fonts, colors, rects, icons):
    """Draw mode selection scene."""
    screen.blit(icons["back"], rects["back_rect"].topleft)
    screen.blit(icons["settings"], rects["settings_icon_rect"].topleft)
    title = fonts["main"].render("Chon che do", True, colors["text_main"])
    screen.blit(title, title.get_rect(center=(panel.centerx, panel.y + 110)))

    def draw_mode_card(rect, icon_primary, icon_secondary, label, color, subtitle):
        pygame.draw.rect(screen, (255, 248, 235), rect, border_radius=16)
        pygame.draw.rect(screen, color, rect, 3, border_radius=16)

        icon_size = min(max(20, rect.height // 3), max(24, rect.width // 5))
        row_y = int(rect.y + rect.height * 0.32)
        gap = max(8, icon_size // 3)
        left_x = rect.centerx - (icon_size + gap // 2)
        right_x = rect.centerx + (gap // 2)
        icon_left = pygame.transform.smoothscale(icon_primary, (icon_size, icon_size))
        icon_right = pygame.transform.smoothscale(icon_secondary, (icon_size, icon_size))
        screen.blit(icon_left, (left_x, row_y - icon_size // 2))
        screen.blit(icon_right, (right_x, row_y - icon_size // 2))

        label_font = pygame.font.SysFont("segoeui", max(18, rect.height // 4), bold=True)
        sub_font = pygame.font.SysFont("segoeui", max(11, min(16, rect.height // 8)))

        shadow = label_font.render(label, True, (24, 20, 18))
        screen.blit(shadow, shadow.get_rect(center=(rect.centerx + 2, int(rect.y + rect.height * 0.70 + 2))))
        text = label_font.render(label, True, color)
        screen.blit(text, text.get_rect(center=(rect.centerx, int(rect.y + rect.height * 0.70))))

        sub_shadow = sub_font.render(subtitle, True, (24, 20, 18))
        screen.blit(sub_shadow, sub_shadow.get_rect(center=(rect.centerx + 1, int(rect.y + rect.height * 0.86 + 1))))
        sub_text = sub_font.render(subtitle, True, (78, 68, 60))
        screen.blit(sub_text, sub_text.get_rect(center=(rect.centerx, int(rect.y + rect.height * 0.86))))

    draw_mode_card(rects["pvp_btn"], icons["mode_pvp"], icons["mode_pvp"], "PvP", colors["btn_blue"], "Nguoi vs nguoi")
    draw_mode_card(rects["pvbot_btn"], icons["mode_pvp"], icons["mode_pvbot"], "PvE", colors["btn_green"], "Nguoi vs bot")
