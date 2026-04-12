"""Choose game mode scene renderer."""

import pygame


def draw_choose_gamemode_scene(screen, panel, fonts, colors, rects, icons):
    """Draw mode selection scene."""
    screen.blit(icons["back"], rects["back_rect"].topleft)
    screen.blit(icons["settings"], rects["settings_icon_rect"].topleft)
    title = fonts["main"].render("Select game mode", True, colors["text_main"])
    screen.blit(title, title.get_rect(center=(panel.centerx, panel.y + 110)))

    def draw_mode_card(rect, icon_surface, label, color):
        pygame.draw.rect(screen, (255, 248, 235), rect, border_radius=16)
        pygame.draw.rect(screen, color, rect, 3, border_radius=16)

        icon_size = min(42, max(30, rect.height // 2))
        icon = pygame.transform.smoothscale(icon_surface, (icon_size, icon_size))
        icon_rect = icon.get_rect(center=(rect.centerx, int(rect.y + rect.height * 0.34)))
        screen.blit(icon, icon_rect)

        label_font = pygame.font.SysFont("segoeui", max(18, rect.height // 4), bold=True)
        sub_font = pygame.font.SysFont("segoeui", max(12, rect.height // 8))

        shadow = label_font.render(label, True, (24, 20, 18))
        screen.blit(shadow, shadow.get_rect(center=(rect.centerx + 2, int(rect.y + rect.height * 0.70 + 2))))
        text = label_font.render(label, True, color)
        screen.blit(text, text.get_rect(center=(rect.centerx, int(rect.y + rect.height * 0.70))))

        subtitle = "Human vs human" if label == "PVP" else "Human vs bot"
        sub_shadow = sub_font.render(subtitle, True, (24, 20, 18))
        screen.blit(sub_shadow, sub_shadow.get_rect(center=(rect.centerx + 1, int(rect.y + rect.height * 0.86 + 1))))
        sub_text = sub_font.render(subtitle, True, (78, 68, 60))
        screen.blit(sub_text, sub_text.get_rect(center=(rect.centerx, int(rect.y + rect.height * 0.86))))

    draw_mode_card(rects["pvp_btn"], icons["mode_pvp"], "PVP", colors["btn_blue"])
    draw_mode_card(rects["pvbot_btn"], icons["mode_pvbot"], "PVBOT", colors["btn_green"])
