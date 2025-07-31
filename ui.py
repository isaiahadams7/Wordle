# ===== ui.py =====

import pygame
from config import (
    WIDTH, HEIGHT, GRID_SIZE, WORD_LENGTH,
    COLORS, FONT_NAME, FONT_SIZE,
    KEYBOARD_ROWS, KEY_FONT_SIZE
)

# Layout constants
TOP_MARGIN    = 80
BOTTOM_MARGIN = 180
PADDING       = 20
GRID_SCALE    = 0.7

# Grid sizing
avail_w   = WIDTH  - 2 * PADDING
avail_h   = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
_raw_cell = min(avail_w // WORD_LENGTH, avail_h // GRID_SIZE)
CELL_SIZE = int(_raw_cell * GRID_SCALE)
GRID_WIDTH  = CELL_SIZE * WORD_LENGTH
GRID_HEIGHT = CELL_SIZE * GRID_SIZE
START_X     = (WIDTH - GRID_WIDTH)  // 2
START_Y     = TOP_MARGIN

# Keyboard sizing
KEY_SPACING = 6
max_keys    = max(len(r) for r in KEYBOARD_ROWS) + 2
KEY_W       = (WIDTH - 2 * PADDING - (max_keys - 1) * KEY_SPACING) // max_keys
KEY_H       = int(KEY_W * 0.6)
KEYBOARD_Y  = START_Y + GRID_HEIGHT + 40

# End-of-game buttons
KB_ROWS      = len(KEYBOARD_ROWS)
KB_HEIGHT    = KB_ROWS * KEY_H + (KB_ROWS - 1) * KEY_SPACING
BUTTON_Y     = KEYBOARD_Y + KB_HEIGHT + 20
BUTTON_W     = 140
BUTTON_H     = 40
BUTTON_SPACE = 20


class GameUI:
    def __init__(self, screen, game):
        self.screen     = screen
        self.game       = game

        # fonts
        self.font        = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.small_font  = pygame.font.SysFont(FONT_NAME, KEY_FONT_SIZE, bold=True)
        self.header_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE + 8, bold=True)

        # transient message
        self.message   = ""
        self.msg_timer = 0

        # keyboard rectangles
        self.key_rects = []

        # end-of-game buttons
        cx = WIDTH // 2
        self.play_again_rect = pygame.Rect(
            cx - BUTTON_W - BUTTON_SPACE//2,
            BUTTON_Y,
            BUTTON_W, BUTTON_H
        )
        self.menu_rect = pygame.Rect(
            cx + BUTTON_SPACE//2,
            BUTTON_Y,
            BUTTON_W, BUTTON_H
        )

    def handle_input(self, event):
        # If game over, only handle clicks on the end-game buttons
        if self.game.is_over():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_again_rect.collidepoint(event.pos):
                    return 'RESTART'
                if self.menu_rect.collidepoint(event.pos):
                    return 'MENU'
            return None

        # Normal keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.game.remove_letter()
            elif event.key == pygame.K_RETURN:
                return self._try_submit()
            else:
                ch = event.unicode
                if ch.isalpha():
                    self.game.add_letter(ch)

        # On-screen keyboard clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for rect, label in self.key_rects:
                if rect.collidepoint(event.pos):
                    if label == 'ENTER':
                        return self._try_submit()
                    elif label == 'BACK':
                        self.game.remove_letter()
                    else:
                        self.game.add_letter(label)
                    break

        return None

    def _try_submit(self):
        success = self.game.submit_guess()
        if not success:
            self.message   = "Not in word list!"
            self.msg_timer = pygame.time.get_ticks() + 2000
        return None

    def draw(self):
        now = pygame.time.get_ticks()
        self.screen.fill(COLORS['bg'])

        # 1) Header
        header_surf = self.header_font.render("ZAY'S WORDLE", True, COLORS['text'])
        header_x    = (WIDTH - header_surf.get_width()) // 2
        header_y    = PADDING // 2
        self.screen.blit(header_surf, (header_x, header_y))

        # 2) Transient message (below header)
        msg_y = header_y + header_surf.get_height() + 10
        if self.message and now < self.msg_timer:
            msg_surf = self.small_font.render(self.message, True, COLORS['text'])
            self.screen.blit(
                msg_surf,
                ((WIDTH - msg_surf.get_width()) // 2, msg_y)
            )
        elif now >= self.msg_timer:
            self.message = ""

        # 3) Grid of guesses
        for row in range(GRID_SIZE):
            if row < len(self.game.guesses):
                guess, status = self.game.guesses[row], self.game.results[row]
            elif row == len(self.game.guesses):
                guess, status = self.game.current_guess, []
            else:
                guess, status = "", []

            for col in range(WORD_LENGTH):
                x = START_X + col * CELL_SIZE
                y = START_Y + row * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE - 5, CELL_SIZE - 5)

                if status:
                    bg = COLORS[status[col]]
                else:
                    bg = COLORS['absent'] if row < len(self.game.guesses) else (58, 58, 60)

                pygame.draw.rect(self.screen, bg, rect, border_radius=5)
                pygame.draw.rect(self.screen, COLORS['text'], rect, 2, border_radius=5)

                letter = guess[col] if col < len(guess) else ""
                if letter:
                    sf = self.font.render(letter.upper(), True, COLORS['text'])
                    tw, th = sf.get_size()
                    self.screen.blit(
                        sf,
                        (x + (CELL_SIZE - tw)//2, y + (CELL_SIZE - th)//2)
                    )

        # 4) End-of-game overlay text
        if self.game.is_over():
            res = "You Win!" if self.game.is_won() else f"Game Over the word was: {self.game.target.upper()}"
            rs = self.small_font.render(res, True, COLORS['text'])
            self.screen.blit(
                rs,
                ((WIDTH - rs.get_width())//2, msg_y)
            )

        # 5) On-screen keyboard
        self.key_rects.clear()
        for ri, row_keys in enumerate(KEYBOARD_ROWS):
            keys = (['ENTER'] + list(row_keys) + ['BACK']) if ri == 2 else list(row_keys)
            total_w = len(keys)*KEY_W + (len(keys)-1)*KEY_SPACING
            sx = (WIDTH - total_w)//2
            y  = KEYBOARD_Y + ri*(KEY_H + KEY_SPACING)

            for key in keys:
                rect = pygame.Rect(sx, y, KEY_W, KEY_H)
                clr  = (160,160,160) if key == 'BACK' else COLORS.get(self.game.key_states.get(key.lower(), ''), (58,58,60))

                pygame.draw.rect(self.screen, clr, rect, border_radius=5)
                pygame.draw.rect(self.screen, COLORS['text'], rect, 2, border_radius=5)

                lbl = '←' if key == 'BACK' else key
                sf  = self.small_font.render(lbl, True, COLORS['text'])
                tw, th = sf.get_size()
                self.screen.blit(
                    sf,
                    (sx + (KEY_W - tw)//2, y + (KEY_H - th)//2)
                )

                self.key_rects.append((rect, key))
                sx += KEY_W + KEY_SPACING

        # 6) Play Again & Menu buttons
        if self.game.is_over():
            # Play Again
            pygame.draw.rect(self.screen, COLORS['text'], self.play_again_rect, border_radius=5)
            inner_pa = self.play_again_rect.inflate(-4, -4)
            pygame.draw.rect(self.screen, COLORS['bg'], inner_pa, border_radius=5)
            pa_s = self.small_font.render("Play Again", True, COLORS['text'])
            px   = self.play_again_rect.x + (BUTTON_W - pa_s.get_width())//2
            py   = self.play_again_rect.y + (BUTTON_H - pa_s.get_height())//2
            self.screen.blit(pa_s, (px, py))

            # Menu
            pygame.draw.rect(self.screen, COLORS['text'], self.menu_rect, border_radius=5)
            inner_m = self.menu_rect.inflate(-4, -4)
            pygame.draw.rect(self.screen, COLORS['bg'], inner_m, border_radius=5)
            m_s = self.small_font.render("Menu", True, COLORS['text'])
            mx  = self.menu_rect.x + (BUTTON_W - m_s.get_width())//2
            my  = self.menu_rect.y + (BUTTON_H - m_s.get_height())//2
            self.screen.blit(m_s, (mx, my))
