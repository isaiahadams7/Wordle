# shop_ui.py

import pygame
from config import WIDTH, HEIGHT, FONT_NAME, FONT_SIZE, KEY_FONT_SIZE, COLORS
from shop import ShopItem

class ShopUI:
    def __init__(self, screen, shop):
        self.screen = screen
        self.shop   = shop

        # fonts
        self.title_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE + 8, bold=True)
        self.font       = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.small_font = pygame.font.SysFont(FONT_NAME, KEY_FONT_SIZE)

        # layout
        self.back_rect = pygame.Rect(10, 10, 80, 30)

        self.item_boxes = []
        box_width  = WIDTH - 200
        box_height = 80
        start_y    = 80
        margin_y   = 20

        for idx, item in enumerate(self.shop.get_catalog()):
            x = 100
            y = start_y + idx * (box_height + margin_y)
            box_rect = pygame.Rect(x, y, box_width, box_height)

            # buy-button on right
            buy_rect = pygame.Rect(
                x + box_width - 90,
                y + (box_height - 30)//2,
                80, 30
            )
            self.item_boxes.append((item, box_rect, buy_rect))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # back to main menu
            if self.back_rect.collidepoint(mx, my):
                return 'BACK'

            # attempt purchase
            for item, box, buy in self.item_boxes:
                if buy.collidepoint(mx, my):
                    if self.shop.can_afford(item.id):
                        self.shop.purchase(item.id)
                    else:
                        # you could flash “Not enough coins” here
                        pass
                    break

        return None

    def draw(self):
        self.screen.fill(COLORS['bg'])

        # title
        title_surf = self.title_font.render("SHOP", True, COLORS['text'])
        tx = (WIDTH - title_surf.get_width()) // 2
        self.screen.blit(title_surf, (tx, 20))

        # balance
        bal = self.shop.get_balance()
        bal_surf = self.font.render(f"Coins: {bal}", True, COLORS['text'])
        self.screen.blit(bal_surf, (WIDTH - bal_surf.get_width() - 20, 20))

        # back button
        pygame.draw.rect(self.screen, COLORS['button_BG'], self.back_rect)
        pygame.draw.rect(self.screen, COLORS['text'], self.back_rect, 2)
        back_s = self.small_font.render("Back", True, COLORS['text'])
        bx = self.back_rect.x + (self.back_rect.w - back_s.get_width())//2
        by = self.back_rect.y + (self.back_rect.h - back_s.get_height())//2
        self.screen.blit(back_s, (bx, by))

        # list items
        inv = self.shop.get_inventory()
        for item, box, buy in self.item_boxes:
            # outline
            pygame.draw.rect(self.screen, COLORS['text'], box, 2)

            # name & description
            name_s = self.font.render(item.name, True, COLORS['text'])
            self.screen.blit(name_s, (box.x + 10, box.y + 8))

            desc_s = self.small_font.render(item.description, True, COLORS['text'])
            self.screen.blit(desc_s, (box.x + 10, box.y + 36))

            # owned count
            owned = inv.get(item.id, 0)
            own_s = self.small_font.render(f"x{owned}", True, COLORS['text'])
            self.screen.blit(own_s, (box.x + 10, box.y + box.h - 24))

            # cost
            cost_s = self.small_font.render(f"{item.cost}¢", True, COLORS['text'])
            self.screen.blit(cost_s, (buy.x - cost_s.get_width() - 10, buy.y + 6))

            # buy button
            pygame.draw.rect(self.screen, COLORS['button_BG'], buy)
            pygame.draw.rect(self.screen, COLORS['text'], buy, 2)
            b_s = self.small_font.render("BUY", True, COLORS['text'])
            bx = buy.x + (buy.w - b_s.get_width())//2
            by = buy.y + (buy.h - b_s.get_height())//2
            self.screen.blit(b_s, (bx, by))
