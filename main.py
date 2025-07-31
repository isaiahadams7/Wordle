# main.py

import pygame
from config    import WIDTH, HEIGHT
from menu_ui   import MenuUI
from stats_ui  import StatsUI
from game      import Game
from ui        import GameUI


def main():
    # Initialize Pygame and the display
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Practice Wordle")
    clock = pygame.time.Clock()

    # Instantiate UI controllers (they each take the screen as argument)
    menu_ui   = MenuUI(screen)
    stats_ui  = StatsUI(screen)
    game      = None
    game_ui   = None

    # State machine: MAIN_MENU -> STATS or GAME
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
                    game    = Game()
                    game_ui = GameUI(screen, game)
                    state   = 'GAME'
                elif action == 'STATS':
                    state = 'STATS'

            elif state == 'STATS':
                action = stats_ui.handle_event(event)
                if action == 'BACK':
                    state = 'MAIN_MENU'

            elif state == 'GAME':
                action = game_ui.handle_input(event)

                # In-game button actions
                if action == 'RESTART':
                    # start a brand new game
                    game    = Game()
                    game_ui = GameUI(screen, game)

                elif action == 'MENU':
                    # return to main menu (drops current game instance)
                    state = 'MAIN_MENU'

        # 2) DRAWING
        if state == 'MAIN_MENU':
            menu_ui.draw()

        elif state == 'STATS':
            stats_ui.draw()

        elif state == 'GAME':
            game_ui.draw()

        # 3) FLIP + FRAME RATE
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
