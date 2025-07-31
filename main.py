# main.py

import pygame
from config    import WIDTH, HEIGHT
from menu_ui   import MenuUI
from stats_ui  import StatsUI
from shop      import Shop
from shop_ui   import ShopUI
from game      import Game
from ui        import GameUI

def main():
    # Initialize Pygame and the display
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Practice Wordle")
    clock = pygame.time.Clock()

    # Set up UI controllers
    menu_ui   = MenuUI(screen)
    stats_ui  = StatsUI(screen)
    shop      = Shop()                 # loads coins & inventory
    shop_ui   = ShopUI(screen, shop)

    game      = None
    game_ui   = None

    # State machine: MAIN_MENU, STATS, SHOP, or GAME
    state     = 'MAIN_MENU'
    running   = True

    while running:
        # 1) EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif state == 'MAIN_MENU':
                action = menu_ui.handle_event(event)
                if action == 'PLAY':
                    # start a new puzzle
                    game    = Game()
                    game.shop = shop           # inject shop for coin awards
                    game_ui = GameUI(screen, game)
                    state   = 'GAME'
                elif action == 'STATS':
                    state = 'STATS'
                elif action == 'SHOP':
                    state = 'SHOP'

            elif state == 'STATS':
                action = stats_ui.handle_event(event)
                if action == 'BACK':
                    state = 'MAIN_MENU'

            elif state == 'SHOP':
                action = shop_ui.handle_event(event)
                if action == 'BACK':
                    state = 'MAIN_MENU'

            elif state == 'GAME':
                action = game_ui.handle_input(event)
                if action == 'RESTART':
                    # replay a fresh puzzle
                    game    = Game()
                    game.shop = shop
                    game_ui = GameUI(screen, game)
                elif action == 'MENU':
                    # back to main menu
                    state = 'MAIN_MENU'

        # 2) DRAWING
        if state == 'MAIN_MENU':
            menu_ui.draw()
        elif state == 'STATS':
            stats_ui.draw()
        elif state == 'SHOP':
            shop_ui.draw()
        elif state == 'GAME':
            game_ui.draw()

        # 3) FLIP + FRAME RATE
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
