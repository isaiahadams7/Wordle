# stats_ui.py

import pygame
import json
import os
from config import WIDTH, HEIGHT, COLORS, FONT_NAME

class StatsUI:
    def __init__(self, screen):
        self.screen     = screen
        self.title_font = pygame.font.SysFont(FONT_NAME, 48, bold=True)
        self.font       = pygame.font.SysFont(FONT_NAME, 32)

        # Back button (top-left)
        self.back_rect  = pygame.Rect(20, 20, 100, 40)

        # Where we persist stats
        self.stats_file = 'stats.json'
        self.wins, self.losses = self._load_stats()

    def _load_stats(self):
        """
        Safely load wins/losses from stats.json.
        Returns (0,0) on missing, empty, or invalid file.
        """
        if not os.path.exists(self.stats_file):
            return 0, 0

        try:
            with open(self.stats_file, 'r') as f:
                data = json.load(f)
            wins   = data.get('wins', 0)
            losses = data.get('losses', 0)
            return wins, losses

        except (json.JSONDecodeError, IOError):
            # empty or corrupted file → reset stats
            return 0, 0

    def _win_pct(self):
        total = self.wins + self.losses
        return (self.wins / total * 100) if total > 0 else 0.0

    def draw(self):
        self.screen.fill(COLORS['bg'])

        # Title
        title_surf = self.title_font.render("Statistics", True, COLORS['text'])
        tx = (WIDTH - title_surf.get_width()) // 2
        ty = HEIGHT // 6
        self.screen.blit(title_surf, (tx, ty))

        # Wins / Losses / Win %
        lines = [
            f"Wins: {self.wins}",
            f"Losses: {self.losses}",
            f"Win %: {self._win_pct():.1f}%"
        ]
        for i, text in enumerate(lines):
            surf = self.font.render(text, True, COLORS['text'])
            x    = (WIDTH - surf.get_width()) // 2
            y    = ty + title_surf.get_height() + 40 + i * (self.font.get_height() + 10)
            self.screen.blit(surf, (x, y))

        # Back button
        pygame.draw.rect(self.screen, COLORS['text'], self.back_rect, border_radius=5)
        inner = self.back_rect.inflate(-4, -4)
        pygame.draw.rect(self.screen, COLORS['bg'], inner, border_radius=5)

        back_surf = self.font.render("Back", True, COLORS['text'])
        bx = self.back_rect.centerx - back_surf.get_width() // 2
        by = self.back_rect.centery - back_surf.get_height() // 2
        self.screen.blit(back_surf, (bx, by))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_rect.collidepoint(event.pos):
                return 'BACK'

        return None
