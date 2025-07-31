# menu_ui.py

import pygame
from config import WIDTH, HEIGHT, COLORS, FONT_NAME

class MenuUI:
    def __init__(self, screen):
        self.screen      = screen

        # Fonts
        self.title_font  = pygame.font.SysFont(FONT_NAME, 72, bold=True)
        self.button_font = pygame.font.SysFont(FONT_NAME, 36, bold=True)

        # Play button (fixed size)
        self.btn_w       = 200
        self.btn_h       = 60
        self.play_rect   = pygame.Rect(
            (WIDTH  - self.btn_w) // 2,
            (HEIGHT // 2),
            self.btn_w,
            self.btn_h
        )

        # Stats button (dynamic size based on text)
        stats_text      = "View Stats"
        self.stats_surf = self.button_font.render(stats_text, True, COLORS['text'])
        padding_x       = 20
        padding_y       = 10
        stats_w         = self.stats_surf.get_width() + padding_x * 2
        stats_h         = self.stats_surf.get_height() + padding_y * 2
        stats_x         = WIDTH - stats_w - 20   # 20px right margin
        stats_y         = 20                     # 20px top margin

        self.stats_rect = pygame.Rect(stats_x, stats_y, stats_w, stats_h)

    def draw(self):
        self.screen.fill(COLORS['bg'])

        # 1) Title
        title_surf = self.title_font.render("Zay’s Wordle", True, COLORS['text'])
        tx = (WIDTH - title_surf.get_width()) // 2
        ty = HEIGHT // 4 - title_surf.get_height() // 2
        self.screen.blit(title_surf, (tx, ty))

        # 2) Play button
        pygame.draw.rect(self.screen, COLORS['text'], self.play_rect, border_radius=8)
        inner_play = self.play_rect.inflate(-6, -6)
        pygame.draw.rect(self.screen, COLORS['bg'], inner_play, border_radius=6)

        play_surf = self.button_font.render("Play", True, COLORS['text'])
        px = self.play_rect.x + (self.play_rect.width  - play_surf.get_width())  // 2
        py = self.play_rect.y + (self.play_rect.height - play_surf.get_height()) // 2
        self.screen.blit(play_surf, (px, py))

        # 3) Stats button
        pygame.draw.rect(self.screen, COLORS['text'], self.stats_rect, border_radius=5)
        inner_stats = self.stats_rect.inflate(-4, -4)
        pygame.draw.rect(self.screen, COLORS['bg'], inner_stats, border_radius=5)

        sx = self.stats_rect.x + (self.stats_rect.width  - self.stats_surf.get_width())  // 2
        sy = self.stats_rect.y + (self.stats_rect.height - self.stats_surf.get_height()) // 2
        self.screen.blit(self.stats_surf, (sx, sy))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_rect.collidepoint(event.pos):
                return 'PLAY'
            if self.stats_rect.collidepoint(event.pos):
                return 'STATS'

        return None
