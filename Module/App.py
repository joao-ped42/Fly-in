import pygame
from pygame import (display, image, time, transform, Surface, RESIZABLE)
from .Scenario import Scenario
from random import choice


class App:
    def __init__(self, scenario: Scenario,
                 screen_w: int,
                 screen_h: int) -> None:
        pygame.init()
        display.set_caption("Fly-in")
        display.set_icon(image.load("src/icon.png"))
        self.scenario: Scenario = scenario
        self.screen: Surface = display.set_mode((screen_w, screen_h),
                                                RESIZABLE)
        self.virtual_screen: Surface = Surface((screen_w, screen_h))
        graph_width: int = int(screen_w * (72.9 / 100))
        self.graph_frame: Surface = Surface((graph_width, screen_h))
        self.menu_frame: Surface = Surface(((screen_w - graph_width),
                                            screen_h))
        self.graph_frame.fill((29, 31, 36))
        self.menu_frame.fill((64, 72, 79))
        bg_imgs: list[str] = ["angel_island",
                              "cosmic_wall",
                              "final_chase",
                              "final_rush",
                              "mad_space",
                              "nika",
                              "sky_chase",
                              "sky_chase2",
                              "skyblock",
                              "tokyo_ghoul",
                              "latios_flying",
                              "rayquaza",
                              "up"]
        bg_img: Surface = image.load(f"src/bg_img/{choice(bg_imgs)}.png")
        self.graph_frame.blit(bg_img)

    def __place_hubs(self) -> None:
        for hub in self.scenario.hubs:
            self.graph_frame.blit(hub.sprite, hub.norm_coord)

    def __place_connections(self) -> None:
        for connection in self.scenario.connections:
            hub1_x: int = connection.point1.norm_coord[0]
            hub2_x: int = connection.point2.norm_coord[0]
            hub1_y: int = connection.point1.norm_coord[1]
            hub2_y: int = connection.point2.norm_coord[1]
            img_size: int = connection.point1.sprite.get_width()
            start_coord_x1: int = int(hub1_x + img_size / 2)
            start_coord_x2: int = int(hub2_x + img_size / 2)
            start_coord_y1: int = int(hub1_y + img_size / 2)
            start_coord_y2: int = int(hub2_y + img_size / 2)
            font: pygame.font.Font = pygame.font.SysFont("Consolas", 30)
            text: Surface = font.render(f"{connection.max_capacity}",
                                        True, (207, 33, 33))
            line_length: int = (max(hub1_x, hub2_x) - min(hub1_x, hub2_x))
            line_height: int = (max(hub1_y, hub2_y) - min(hub1_y, hub2_y))
            text_x: int = (line_length / 2) + min(hub1_x, hub2_x)
            text_y: int = (line_height / 2) + min(hub1_y, hub2_y)
            print(text_x)
            print(text_y)
            pygame.draw.line(self.graph_frame,
                             (255, 255, 255),
                             (start_coord_x1, start_coord_y1),
                             (start_coord_x2, start_coord_y2), 3)
            self.graph_frame.blit(text, (text_x, text_y))

    def __place_drones(self) -> None:
        for drone in self.scenario.drones:
            hub_size: int = self.scenario.hubs[0].sprite.get_width()
            new_size: tuple[int, int] = ((hub_size - 10), (hub_size - 10))
            resized_drone: Surface = transform.scale(drone.sprite, new_size)
            dest: tuple[int, int] = (drone.norm_x, drone.norm_y)
            self.graph_frame.blit(resized_drone, dest)

    def run(self) -> None:
        clock: time.Clock = time.Clock()
        running: bool = True
        while (running):
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    running = False
            self.__place_connections()
            self.__place_hubs()
            self.__place_drones()
            self.virtual_screen.blit(self.graph_frame, (0, 0))
            self.virtual_screen.blit(self.menu_frame, (1400, 0))
            current_w: int = self.screen.get_width()
            current_h: int = self.screen.get_height()
            scaled: Surface = transform.scale(self.virtual_screen,
                                              (current_w, current_h))
            self.screen.blit(scaled)
            display.flip()
            clock.tick(60)
        pygame.quit()
