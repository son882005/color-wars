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

        icon_rect = icon_surface.get_rect(midleft=(rect.x + 58, rect.centery))
        screen.blit(icon_surface, icon_rect)

        shadow = fonts["button"].render(label, True, (24, 20, 18))
        screen.blit(shadow, shadow.get_rect(center=(rect.centerx + 2, rect.centery + 2)))
        text = fonts["button"].render(label, True, color)
        screen.blit(text, text.get_rect(center=rect.center))

    draw_mode_card(rects["pvp_btn"], icons["mode_pvp"], "PVP", colors["btn_blue"])
    draw_mode_card(rects["pvbot_btn"], icons["mode_pvbot"], "PVBOT", colors["btn_green"])
