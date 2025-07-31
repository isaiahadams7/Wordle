# main.py
import pygame
from config import WIDTH, HEIGHT
from game import Game, load_word_list
from ui import GameUI

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle Remake")
clock = pygame.time.Clock()

# Initialize game
word_list = load_word_list()
game = Game(word_list)
ui = GameUI(screen, game)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and not game.is_over():
            ui.handle_input(event)

    ui.draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
