# ui.py
import pygame
from config import WIDTH, HEIGHT, GRID_SIZE, WORD_LENGTH, COLORS, FONT_NAME, FONT_SIZE

# Margins and available space
PADDING = 20
AVAILABLE_WIDTH = WIDTH - 2 * PADDING
AVAILABLE_HEIGHT = HEIGHT - 2 * PADDING

# Compute square size so it fits both dimensions
CELL_SIZE = min(
    AVAILABLE_WIDTH // WORD_LENGTH,
    AVAILABLE_HEIGHT // GRID_SIZE
)

# Actual grid pixel dimensions
GRID_WIDTH = CELL_SIZE * WORD_LENGTH
GRID_HEIGHT = CELL_SIZE * GRID_SIZE

# Top-left corner of the grid to center it
START_X = (WIDTH - GRID_WIDTH) // 2
START_Y = (HEIGHT - GRID_HEIGHT) // 2

class GameUI:
    def __init__(self, screen, game):
        self.screen     = screen
        self.game       = game
        self.font       = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.small_font = pygame.font.SysFont(FONT_NAME, 24)
        self.message    = ""
        self.msg_timer  = 0

    def handle_input(self, event):
        # Ignore input if the game is over
        if self.game.is_over():
            return

        if event.key == pygame.K_BACKSPACE:
            self.game.remove_letter()

        elif event.key == pygame.K_RETURN:
            success = self.game.submit_guess()
            if not success:
                self.message   = "Invalid guess!"
                self.msg_timer = pygame.time.get_ticks() + 2000  # show for 2s

        else:
            char = event.unicode
            if char.isalpha():
                self.game.add_letter(char)

    def draw(self):
        # Clear screen
        self.screen.fill(COLORS['bg'])

        # Show transient message (up to 2 seconds)
        now = pygame.time.get_ticks()
        if self.message and now < self.msg_timer:
            msg_surf = self.small_font.render(self.message, True, COLORS['text'])
            self.screen.blit(
                msg_surf,
                ((WIDTH - msg_surf.get_width()) // 2, START_Y - 40)
            )
        elif now >= self.msg_timer:
            self.message = ""

        # Draw the grid of tiles
        for row in range(GRID_SIZE):
            if row < len(self.game.guesses):
                guess  = self.game.guesses[row]
                status = self.game.results[row]
            elif row == len(self.game.guesses):
                guess  = self.game.current_guess
                status = []
            else:
                guess  = ""
                status = []

            for col in range(WORD_LENGTH):
                x = START_X + col * CELL_SIZE
                y = START_Y + row * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE - 5, CELL_SIZE - 5)

                # Determine tile color
                if status:
                    color = COLORS[status[col]]
                else:
                    if row < len(self.game.guesses):
                        color = COLORS['absent']
                    else:
                        color = (58, 58, 60)

                pygame.draw.rect(self.screen, color, rect, border_radius=5)
                pygame.draw.rect(self.screen, COLORS['text'], rect, 2, border_radius=5)

                # Render letter if present
                letter = guess[col] if col < len(guess) else ""
                if letter:
                    txt_surf = self.font.render(letter.upper(), True, COLORS['text'])
                    tw, th   = txt_surf.get_size()
                    self.screen.blit(
                        txt_surf,
                        (x + (CELL_SIZE - tw) // 2, y + (CELL_SIZE - th) // 2)
                    )

        # Draw end-of-game message
        if self.game.is_over():
            if self.game.is_won():
                result = "You Win!"
            else:
                result = f"Game Over: {self.game.target.upper()}"
            res_surf = self.small_font.render(result, True, COLORS['text'])
            self.screen.blit(
                res_surf,
                ((WIDTH - res_surf.get_width()) // 2, START_Y - 80)
            )
