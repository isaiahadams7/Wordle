# boost_ui.py

import pygame
from config import WIDTH, HEIGHT, COLORS, FONT_NAME
from shop import CATALOG

class BoostUI:
    def __init__(self, screen, shop):
        """
        screen : your pygame display surface
        shop   : instance of shop.Shop
        """
        self.screen = screen
        self.shop   = shop

        # common font
        self.font = pygame.font.SysFont(FONT_NAME, 24, bold=True)

        # build one entry per catalog item
        self.boosts = []
        btn_w, btn_h = 140, 40
        spacing      = 20
        total_w      = len(CATALOG) * btn_w + (len(CATALOG)-1) * spacing
        start_x      = (WIDTH - total_w) // 2
        y_pos        = HEIGHT - btn_h - 20

        for idx, (item_id, item) in enumerate(CATALOG.items()):
            x = start_x + idx * (btn_w + spacing)
            rect = pygame.Rect(x, y_pos, btn_w, btn_h)
            label_surf = self.font.render(item.name, True, COLORS['text'])
            self.boosts.append({
                'id':     item_id,
                'rect':   rect,
                'label':  label_surf
            })

    def draw(self):
        inv = self.shop.get_inventory()

        for b in self.boosts:
            rect = b['rect']

            # outer & inner boxes
            pygame.draw.rect(self.screen, COLORS['text'], rect, border_radius=6)
            inner = rect.inflate(-4, -4)
            pygame.draw.rect(self.screen, COLORS['bg'], inner, border_radius=6)

            # draw label
            lx = rect.x + (rect.w - b['label'].get_width()) // 2
            ly = rect.y + 4
            self.screen.blit(b['label'], (lx, ly))

            # draw count below
            count = inv.get(b['id'], 0)
            cnt_surf = self.font.render(f"x{count}", True, COLORS['text'])
            cx = rect.x + (rect.w - cnt_surf.get_width()) // 2
            cy = ly + b['label'].get_height() + 2
            self.screen.blit(cnt_surf, (cx, cy))

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        pos = event.pos
        inv = self.shop.get_inventory()

        for b in self.boosts:
            if b['rect'].collidepoint(pos) and inv.get(b['id'], 0) > 0:
                return b['id']

        return None
