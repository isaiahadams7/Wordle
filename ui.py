# ui.py

import pygame
from config import (
    WIDTH, HEIGHT, GRID_SIZE, WORD_LENGTH,
    COLORS, FONT_NAME, FONT_SIZE,
    KEYBOARD_ROWS, KEY_FONT_SIZE
)

# Layout constants
TOP_MARGIN    = 80    # space for header & messages
BOTTOM_MARGIN = 180   # space for on-screen keyboard
PADDING       = 20    # left/right padding
GRID_SCALE    = 0.7   # shrink grid to fit

# Compute available area for the grid
avail_w = WIDTH  - 2 * PADDING
avail_h = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
_raw_cell = min(avail_w // WORD_LENGTH, avail_h // GRID_SIZE)
CELL_SIZE   = int(_raw_cell * GRID_SCALE)
GRID_WIDTH  = CELL_SIZE * WORD_LENGTH
GRID_HEIGHT = CELL_SIZE * GRID_SIZE
START_X     = (WIDTH - GRID_WIDTH) // 2
START_Y     = TOP_MARGIN

# Keyboard sizing
KEY_SPACING  = 6
max_keys     = max(len(r) for r in KEYBOARD_ROWS) + 2  # +2 for Enter/Back
KEY_W        = (WIDTH - 2 * PADDING - (max_keys - 1) * KEY_SPACING) // max_keys
KEY_H        = int(KEY_W * 0.6)
KEYBOARD_Y   = START_Y + GRID_HEIGHT + 40

# Styling constants
HEADER_FONT_SIZE = 64
BACK_BG_COLOR    = (160, 160, 160)


class GameUI:
    def __init__(self, screen, game):
        self.screen     = screen
        self.game       = game

        self.header_font = pygame.font.SysFont(FONT_NAME, HEADER_FONT_SIZE, bold=True)
        self.font        = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.small_font  = pygame.font.SysFont(FONT_NAME, KEY_FONT_SIZE, bold=True)

        self.message    = ""
        self.msg_timer  = 0
        self.key_rects  = []  # list of (pygame.Rect, label)

    def handle_input(self, event):
        if self.game.is_over():
            # you can still click Enter/BACK after game over
            pass

        # physical keyboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.game.remove_letter()
            elif event.key == pygame.K_RETURN:
                self._try_submit()
            else:
                ch = event.unicode
                if ch.isalpha():
                    self.game.add_letter(ch)

        # mouse click on on-screen keys
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for rect, label in self.key_rects:
                if rect.collidepoint(event.pos):
                    if label == 'ENTER':
                        self._try_submit()
                    elif label == 'BACK':
                        self.game.remove_letter()
                    else:
                        self.game.add_letter(label)
                    break

    def _try_submit(self):
        success = self.game.submit_guess()
        if not success:
            self.message   = "Not in word list!"
            self.msg_timer = pygame.time.get_ticks() + 2000

    def draw(self):
        now = pygame.time.get_ticks()
        self.screen.fill(COLORS['bg'])

        # 1) WORDLE header
        header_surf = self.header_font.render("ZAY'S WORDLE", True, COLORS['text'])
        header_x    = (WIDTH - header_surf.get_width()) // 2
        header_y    = PADDING // 2
        self.screen.blit(header_surf, (header_x, header_y))

        # 2) Transient message below header
        msg_y = header_y + header_surf.get_height() + 10
        if self.message and now < self.msg_timer:
            msg_surf = self.small_font.render(self.message, True, COLORS['text'])
            self.screen.blit(
                msg_surf,
                ((WIDTH - msg_surf.get_width()) // 2, msg_y)
            )
        elif now >= self.msg_timer:
            self.message = ""

        # 3) Draw grid
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
                r = pygame.Rect(x, y, CELL_SIZE - 5, CELL_SIZE - 5)

                if status:
                    color = COLORS[status[col]]
                else:
                    color = COLORS['absent'] if row < len(self.game.guesses) else (58,58,60)

                pygame.draw.rect(self.screen, color, r, border_radius=5)
                pygame.draw.rect(self.screen, COLORS['text'], r, 2, border_radius=5)

                letter = guess[col] if col < len(guess) else ""
                if letter:
                    surf = self.font.render(letter.upper(), True, COLORS['text'])
                    tw, th = surf.get_size()
                    self.screen.blit(
                        surf,
                        (x + (CELL_SIZE - tw)//2, y + (CELL_SIZE - th)//2)
                    )

        # 4) End-of-game message (overwrites transient if ended)
        if self.game.is_over():
            result = "You Win!" if self.game.is_won() else f"Game Over: {self.game.target.upper()}"
            res_surf = self.small_font.render(result, True, COLORS['text'])
            self.screen.blit(
                res_surf,
                ((WIDTH - res_surf.get_width()) // 2, msg_y)
            )

        # 5) On-screen keyboard
        self.key_rects.clear()
        for row_idx, row_keys in enumerate(KEYBOARD_ROWS):
            # on 3rd row insert Enter and BACK
            keys = list(row_keys)
            if row_idx == 2:
                keys = ['ENTER'] + keys + ['BACK']

            row_len     = len(keys)
            total_w     = row_len * KEY_W + (row_len - 1) * KEY_SPACING
            start_x     = (WIDTH - total_w) // 2
            y           = KEYBOARD_Y + row_idx * (KEY_H + KEY_SPACING)

            for i, key in enumerate(keys):
                x    = start_x + i * (KEY_W + KEY_SPACING)
                rect = pygame.Rect(x, y, KEY_W, KEY_H)

                # pick key color (override BACK)
                if key == 'BACK':
                    color = BACK_BG_COLOR
                else:
                    st    = self.game.key_states.get(key.lower())
                    color = COLORS[st] if st in COLORS else (58,58,60)

                pygame.draw.rect(self.screen, color, rect, border_radius=5)
                pygame.draw.rect(self.screen, COLORS['text'], rect, 2, border_radius=5)

                label = '⌫' if key == 'BACK' else key
                surf  = self.small_font.render(label, True, COLORS['text'])
                tw, th = surf.get_size()
                self.screen.blit(
                    surf,
                    (x + (KEY_W - tw)//2, y + (KEY_H - th)//2)
                )

                self.key_rects.append((rect, key))
