from Module import Scenario, App
from Module.Factory import Factory
from sys import argv
import pygame


def main() -> None:
    # try:
    pygame.init()
    info: pygame.display._VidInfo = pygame.display.Info()
    screen_width: int = int(info.current_w)
    screen_height: int = int(info.current_h * (87.6 / 100))
    naruto: Scenario = Factory().read_file(argv[1],
                                           screen_width,
                                           screen_height)
    app: App = App(naruto, screen_width, screen_height)
    app.run()
    # except Exception as e:
    #     print(e)


if (__name__ == "__main__"):
    main()
