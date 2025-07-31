# main.py
import pygame
from config import WIDTH, HEIGHT
from game import Game
from ui import GameUI

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Zay's Wordle")
    clock = pygame.time.Clock()

    game = Game()
    ui   = GameUI(screen, game)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                ui.handle_input(event)

        ui.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
