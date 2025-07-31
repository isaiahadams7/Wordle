import pygame
from config    import WIDTH, HEIGHT
from menu_ui   import MenuUI
from stats_ui  import StatsUI
from game      import Game
from ui        import GameUI

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Zay’s Wordle")
    clock  = pygame.time.Clock()

    # Instantiate screens
    menu       = MenuUI(screen)
    stats_view = StatsUI(screen)

    # 1) Home menu loop
    in_menu    = True
    menu_state = 'MAIN'

    while in_menu:
        for event in pygame.event.get():
            if menu_state == 'MAIN':
                action = menu.handle_event(event)
                if action == 'PLAY':
                    in_menu = False
                elif action == 'STATS':
                    menu_state = 'STATS'

            elif menu_state == 'STATS':
                action = stats_view.handle_event(event)
                if action == 'BACK':
                    menu_state = 'MAIN'

        # Render
        if menu_state == 'MAIN':
            menu.draw()
        else:
            stats_view.draw()

        pygame.display.flip()
        clock.tick(60)

    # 2) Launch the actual game
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
