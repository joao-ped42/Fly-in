import pygame
from sys import argv
from Module import Scenario, App
from Module.Factory import Factory


def main() -> None:
    try:
        pygame.init()
        screen_info: pygame.display._VidInfo = pygame.display.Info()
        screen_width: int = int(screen_info.current_w)
        screen_height: int = int(screen_info.current_h * (87.6 / 100))
        scenario: Scenario = Factory().read_file(argv[1],
                                                 screen_width,
                                                 screen_height)
        app: App = App(scenario, screen_width, screen_height)
        app.display_solution()
        app.run()
    except KeyboardInterrupt:
        print("\nVocê podia só ter fechado a janela, mas tudo bem", end="")


if (__name__ == "__main__"):
    main()
