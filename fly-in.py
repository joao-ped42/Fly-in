from Module import Scenario, App
from Module.Factory import Factory
from sys import argv
import pygame


def main() -> None:
    try:
        pygame.init()
        print()
        screen_info: pygame.display._VidInfo = pygame.display.Info()
        screen_width: int = int(screen_info.current_w)
        screen_height: int = int(screen_info.current_h * (87.6 / 100))
        naruto: Scenario = Factory().read_file(argv[1],
                                               screen_width,
                                               screen_height)
        app: App = App(naruto, screen_width, screen_height)
        app.scenario.visitable_neighbours(app.scenario.hubs[0])
        app.display_solution()
        app.run()
    except KeyboardInterrupt:
        print("\nVocê podia só ter fechado a janela, mas tudo bem", end="")


if (__name__ == "__main__"):
    main()
