import pygame
from random import choice
from .Scenario import Scenario
from .Types import Colors, Color
from .utils import Drone, Adjuster
from pygame import (display, image, time, transform, Surface, RESIZABLE)


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
        self.graph_width: int = int(screen_w * (72.9 / 100))
        self.graph_frame: Surface = Surface((self.graph_width, screen_h))
        self.menu_frame: Surface = Surface(((screen_w - self.graph_width),
                                            screen_h))
        self.graph_frame.fill((29, 31, 36))
        self.menu_frame.fill((64, 72, 79))
        bg_imgs: dict[str, Colors] = {"angel_island": ((255, 243, 163),
                                                       (31, 99, 209)),
                                      "cosmic_wall": ((240, 199, 53),
                                                      (199, 97, 24)),
                                      "final_chase": ((0, 0, 0),
                                                      (0, 0, 0)),
                                      "final_rush": ((0, 0, 0),
                                                     (0, 0, 0)),
                                      "mad_space": ((0, 0, 0),
                                                    (0, 0, 0)),
                                      "nika": ((0, 0, 0),
                                               (0, 0, 0)),
                                      "sky_chase": ((0, 0, 0),
                                                    (0, 0, 0)),
                                      "sky_chase2": ((0, 0, 0),
                                                     (0, 0, 0)),
                                      "skyblock": ((0, 0, 0),
                                                   (0, 0, 0)),
                                      "tokyo_ghoul": ((0, 0, 0),
                                                      (0, 0, 0)),
                                      "latios_flying": ((0, 0, 0),
                                                        (0, 0, 0)),
                                      "rayquaza": ((0, 0, 0),
                                                   (0, 0, 0)),
                                      "up": ((0, 0, 0),
                                             (0, 0, 0))}
        bg_choice: tuple[str, Colors] = choice(tuple(bg_imgs.items()))
        self.bg_img: Surface = image.load(f"src/bg_img/{bg_choice[0]}.png")
        self.text_color: Color = bg_choice[1][0]
        self.connec_color: Color = bg_choice[1][1]

    def __place_hubs(self) -> None:
        for hub in self.scenario.hubs:
            self.graph_frame.blit(hub.sprite, hub.norm_coord)

    def __place_hub_names(self) -> None:
        for hub in self.scenario.hubs:
            hub_size: int = hub.sprite.get_width()
            font_size: int = int(hub_size / 5)
            font: pygame.font.Font = pygame.font.SysFont("Consolas", font_size)
            text: Surface = font.render(hub.name, True, self.text_color)
            text_w: int = text.get_width()
            text_x: int = int((hub.norm_coord[0] + (hub_size / 2))
                              - (text_w / 2))
            text_y: int = hub_size + hub.norm_coord[1]
            self.graph_frame.blit(text, (text_x, text_y))

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
            pygame.draw.line(self.graph_frame,
                             self.connec_color,
                             (start_coord_x1, start_coord_y1),
                             (start_coord_x2, start_coord_y2), 3)

    def __place_drones(self) -> None:
        for drone in self.scenario.drones:
            hub_size: int = self.scenario.hubs[0].sprite.get_width()
            new_size: tuple[int, int] = ((hub_size - 20), (hub_size - 20))
            resized_drone: Surface = transform.scale(drone.sprite, new_size)
            dest: tuple[int, int] = (drone.norm_x, drone.norm_y)
            self.graph_frame.blit(resized_drone, dest)

    def __move_drone(self, drone: Drone) -> None:
        if ((drone.norm_x, drone.norm_y) != drone.current_hub.norm_coord):
            move_values: tuple[int, int] = Adjuster.variation_rate(drone.norm_x,
                                                                   drone.norm_y,
                                                                   drone.current_hub.norm_coord[0],
                                                                   drone.current_hub.norm_coord[1])
            drone.move(move_values[0], move_values[1])

    def run(self) -> None:
        clock: time.Clock = time.Clock()
        running: bool = True
        drone: Drone = self.scenario.drones[0]
        drone.move_to_hub(self.scenario.hubs[1])
        while (running):
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    running = False
            # if (drone.norm_x != 305):
            #     print(drone.norm_x)
            self.graph_frame.blit(self.bg_img)
            self.__move_drone(drone)
            self.__place_connections()
            self.__place_hubs()
            self.__place_hub_names()
            self.__place_drones()
            self.virtual_screen.blit(self.graph_frame, (0, 0))
            self.virtual_screen.blit(self.menu_frame, (self.graph_width, 0))
            current_w: int = self.screen.get_width()
            current_h: int = self.screen.get_height()
            scaled: Surface = transform.scale(self.virtual_screen,
                                              (current_w, current_h))
            self.screen.blit(scaled)
            display.flip()
            clock.tick(60)
        pygame.quit()
