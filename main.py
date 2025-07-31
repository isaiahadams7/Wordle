# main.py

import pygame
from config      import WIDTH, HEIGHT
from menu_ui     import MenuUI
from stats_ui    import StatsUI
from shop        import Shop
from shop_ui     import ShopUI
from game        import Game
from ui          import GameUI
from boost_ui    import BoostUI   # <-- new import

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Practice Wordle")
    clock = pygame.time.Clock()

    # UI + data controllers
    menu_ui  = MenuUI(screen)
    stats_ui = StatsUI(screen)
    shop     = Shop()                 # loads coins & boost counts
    shop_ui  = ShopUI(screen, shop)

    game     = None
    game_ui  = None
    boost_ui = None                   # initialize placeholder

    state    = 'MAIN_MENU'
    running  = True

    while running:
        # 1) EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # —— Main Menu
            elif state == 'MAIN_MENU':
                action = menu_ui.handle_event(event)
                if action == 'PLAY':
                    # start a fresh game
                    game    = Game()
                    game.shop = shop       # give game access to inventory
                    game_ui   = GameUI(screen, game)
                    boost_ui  = BoostUI(screen, shop)
                    state     = 'GAME'

                elif action == 'STATS':
                    state = 'STATS'

                elif action == 'SHOP':
                    state = 'SHOP'

            # —— Stats Screen
            elif state == 'STATS':
                action = stats_ui.handle_event(event)
                if action == 'BACK':
                    state = 'MAIN_MENU'

            # —— Shop Screen
            elif state == 'SHOP':
                action = shop_ui.handle_event(event)
                if action == 'BACK':
                    state = 'MAIN_MENU'

            # —— In‐Game
            elif state == 'GAME':
                # 1a) Wordle input (letters, enter, backspace, menu, restart…)
                action = game_ui.handle_input(event)
                if action == 'RESTART':
                    game    = Game()
                    game.shop = shop
                    game_ui   = GameUI(screen, game)
                    boost_ui  = BoostUI(screen, shop)

                elif action == 'MENU':
                    state = 'MAIN_MENU'

                boost_key = boost_ui.handle_event(event)
                if boost_key:
                    # Delegates inventory check, decrement, and effect application
                    shop.use(boost_key, game)

        # 2) DRAWING
        if state == 'MAIN_MENU':
            menu_ui.draw()

        elif state == 'STATS':
            stats_ui.draw()

        elif state == 'SHOP':
            shop_ui.draw()

        elif state == 'GAME':
            game_ui.draw()      # draws board + keyboard
            boost_ui.draw()     # draws your new buttons below the keyboard

        # 3) FLIP + FRAME RATE
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
