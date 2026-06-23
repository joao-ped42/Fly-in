from .objs.Hub import Hub
from .Scenario import Scenario
from .utils import Drone, Adjuster
from .Types import Colors, Color, Paths, Coord, Hubs
import os
import pygame
from time import sleep
from random import choice
from pygame.mixer import Sound
from collections.abc import Callable
from pygame import (display, image, time,
                    transform, Surface, RESIZABLE,
                    mixer)


class App:
    def __init__(self, scenario: Scenario,
                 screen_w: int,
                 screen_h: int) -> None:
        pygame.init()
        mixer.init()
        display.set_caption("Fly-in")
        display.set_icon(image.load("src/icon.png"))
        self.scenario: Scenario = scenario
        self.solution: Paths = self.scenario.solved_path()
        self.screen: Surface = display.set_mode((screen_w, screen_h),
                                                RESIZABLE)
        self.virtual_screen: Surface = Surface((screen_w, screen_h))
        self.graph_frame: Surface = Surface((screen_w, screen_h))
        self.graph_frame.fill((29, 31, 36))
        bg_imgs: dict[str, Colors] = {"angel_island": ((245, 177, 32),
                                                       (24, 204, 78)),
                                      "biolizard": ((55, 74, 69),
                                                    (214, 135, 71)),
                                      "cosmic_wall": ((158, 45, 173),
                                                      (199, 97, 24)),
                                      "final_chase": ((22, 217, 158),
                                                      (196, 135, 37)),
                                      "final_rush": ((245, 177, 32),
                                                     (255, 255, 255)),
                                      "mad_space": ((74, 26, 122),
                                                    (22, 199, 99)),
                                      "nika": ((0, 0, 0),
                                               (255, 255, 255)),
                                      "sky_chase": ((41, 72, 87),
                                                    (227, 113, 52)),
                                      "sky_chase2": ((245, 177, 32),
                                                     (138, 28, 31)),
                                      "skyblock": ((51, 36, 21),
                                                   (255, 255, 255)),
                                      "tokyo_ghoul": ((0, 0, 0),
                                                      (10, 16, 138)),
                                      "latios_flying": ((44, 171, 74),
                                                        (161, 93, 31)),
                                      "rayquaza": ((199, 40, 201),
                                                   (60, 209, 38)),
                                      "up": ((0, 0, 0),
                                             (255, 255, 255)),
                                      "walpurgisnatch": ((156, 50, 103),
                                                         (180, 133, 242))}
        bg_choice: tuple[str, Colors] = choice(tuple(bg_imgs.items()))
        self.bg_img: Surface = image.load(f"src/bg_img/{bg_choice[0]}.png")
        self.text_color: Color = bg_choice[1][0]
        self.connec_color: Color = bg_choice[1][1]
        self.menu: Surface = Surface((self.virtual_screen.get_width() / 2,
                                      self.virtual_screen.get_height() * 3/4))
        self.music: str = bg_choice[0]
        self.running: bool = True

    def run(self) -> None:
        def _() -> None:
            sprites: list[str] = []
            folder: str = "src/vid"
            for sprite in os.listdir(folder):
                full_path: str = os.path.join(folder, sprite)
                if (os.path.isfile(full_path)):
                    sprites.append(f"{folder}/{sprite}")
            sprites = list(sorted(sprites))
            display.flip()
            sound: mixer.Sound = mixer.Sound("src/_.mp3")
            sound.set_volume(3.0)
            overlay: Surface = Surface((self.virtual_screen.get_width(),
                                        self.virtual_screen.get_height()),
                                       pygame.SRCALPHA)
            pygame.mixer.music.set_volume(0)
            sleep(3)
            sound.play()
            for f in sprites:
                img: Surface = image.load(f)
                s_w: int = self.virtual_screen.get_width()
                s_h: int = self.virtual_screen.get_height()
                resize: Surface = transform.scale(img, (s_w, s_h))
                img_w: int = resize.get_width()
                img_h: int = resize.get_height()
                dest: Coord = (int(s_w / 2) - int(img_w / 2),
                               int(s_h / 2) - int(img_h / 2))
                self.virtual_screen.blit(resize, dest)
                current_w: int = self.screen.get_width()
                current_h: int = self.screen.get_height()
                scaled: Surface = transform.scale(self.virtual_screen,
                                                  (current_w, current_h))
                self.screen.blit(scaled)
                display.flip()
                self.graph_frame.blit(self.bg_img, (0, 0))
                self.virtual_screen.blit(self.graph_frame, (0, 0))
                self.__place_sound(sound_text)
                self.virtual_screen.blit(overlay, (0, 0))
            sound.stop()
            pygame.mixer.music.set_volume(0.2)
        mixer.music.load(f"src/msc/{self.music}.mp3")
        mixer.music.set_volume(0.2)
        clock: time.Clock = time.Clock()
        drone_size: int = self.scenario.drones[0].drone_size
        hub_size: int = self.scenario.hubs[0].sprite.get_width()
        sol_index: int = 0
        center: Callable[[int, int, Coord], Coord] = Adjuster.centralize_drone
        recent_hub: Hub = self.scenario.get_start_hub()
        pygame.mixer.music.play(-1)
        sound: str = "On"
        font: pygame.Font = pygame.font.SysFont("Consolas", 50, bold=True)
        _counter: int = 0
        turn: int = 0
        direction: str = "right"
        self.scenario.drones[0].waiting = False
        while (self.running):
            bet: int = choice(range(100000))
            if ((bet == 67) and (_counter == 0)):
                _()
                _counter += 1
            sound_text: Surface = font.render(f"Sound: {sound}",
                                              True, self.text_color)
            turn_text: Surface = font.render(f"Turn: {turn}",
                                             True, self.text_color)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    self.running = False
                elif (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_SPACE):
                        pygame.mixer.music.pause()
                        menu_sound: Sound = Sound("src/menu_pause.wav")
                        menu_sound.set_volume(0.5)
                        menu_sound.play()
                        self.__place_menu(sound_text, direction)
                        menu_sound.play()
                        pygame.mixer.music.unpause()
                    if (event.key == pygame.K_m):
                        if (pygame.mixer.music.get_volume() > 0):
                            pygame.mixer.music.set_volume(0)
                            sound = "Off"
                        else:
                            pygame.mixer.music.set_volume(0.2)
                            sound = "On"
                    elif (event.key == pygame.K_KP_MINUS):
                        volume: float = pygame.mixer.music.get_volume()
                        new: float = max(0.0, volume - 0.1)
                        pygame.mixer.music.set_volume(new)
                        if (new == 0):
                            sound = "Off"
                    elif (event.key == pygame.K_KP_PLUS):
                        volume = pygame.mixer.music.get_volume()
                        new = min(2.0, volume + 0.1)
                        pygame.mixer.music.set_volume(new)
                        sound = "On"
                    elif (event.key == pygame.K_ESCAPE):
                        self.running = False
                    elif (event.key == pygame.K_RIGHT):
                        if (choice(range(100)) == 67):
                            _()
                        for i in range(len(self.solution)):
                            drone: Drone = self.scenario.drones[i]
                            sol: Hubs = self.solution[i]
                            hub_coords: Coord = drone.current_hub.norm_coord
                            recent_coords: Coord = (drone.norm_x, drone.norm_y)
                            if (recent_coords == center(hub_size,
                                                        drone_size,
                                                        hub_coords)):
                                if (sol_index < len(sol) - 1):
                                    try:
                                        sol_index += 1
                                        hub = sol[sol_index]
                                        if (drone.current_hub.coordinates[0]
                                                < hub.coordinates[0]):
                                            direction = "right"
                                        if (hub.zone == "restricted"):
                                            turn += 2
                                        else:
                                            turn += 1
                                        recent_hub = drone.current_hub
                                        drone.move_to_hub(hub)
                                    except IndexError:
                                        pass
                    elif (event.key == pygame.K_LEFT):
                        for i in range(len(self.solution)):
                            drone = self.scenario.drones[i]
                            sol = self.solution[i]
                            hub_coords = (drone.norm_x, drone.norm_y)
                            n_coord: Coord = drone.current_hub.norm_coord
                            if (hub_coords == center(hub_size,
                                                    drone.drone_size,
                                                    n_coord)):
                                try:
                                    if (sol_index > 0):
                                        zone: str = drone.current_hub.zone
                                        if (zone == "restricted"):
                                            turn -= 2
                                        else:
                                            turn -= 1
                                        recent_hub = drone.current_hub
                                        sol_index -= 1
                                        hub = sol[sol_index]
                                        if (drone.current_hub.coordinates[0] >
                                                hub.coordinates[0]):
                                            direction = "left"
                                        drone.move_to_hub(hub)
                                except IndexError:
                                    pass
            self.graph_frame.blit(self.bg_img)
            for recent_drone in self.scenario.drones:
                if (not recent_drone.waiting):
                    self.__move_drone(recent_drone, recent_hub)
            self.__place_connections()
            self.__place_hubs()
            self.__place_hub_names()
            self.__place_drones(direction)
            self.__place_sound(sound_text)
            self.__place_turn(turn_text)
            self.virtual_screen.blit(self.graph_frame, (0, 0))
            self.__resize()
            display.flip()
            self.virtual_screen.fill((0, 0, 0))
            # sleep(0.05)
            clock.tick(60)
        pygame.quit()

    def __place_hubs(self) -> None:
        for hub in self.scenario.hubs:
            self.graph_frame.blit(hub.sprite, hub.norm_coord)

    def __place_hub_names(self) -> None:
        for hub in self.scenario.hubs:
            hub_size: int = hub.sprite.get_width()
            font_size: int = int(hub_size / 5)
            font: pygame.font.Font = pygame.font.SysFont("Consolas",
                                                         font_size,
                                                         bold=True)
            text: Surface = font.render(hub.name, True, self.text_color)
            text_w: int = text.get_width()
            text_x: int = int((hub.norm_coord[0] + (hub_size / 2))
                              - (text_w / 2))
            text_y: int = hub_size + hub.norm_coord[1]
            if (text_y >= self.virtual_screen.get_height()):
                text_y = hub.norm_coord[1] - text.get_height()
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
                             (start_coord_x2, start_coord_y2),
                             int(img_size / 10))

    def __place_drones(self, direction: str) -> None:
        for drone in self.scenario.drones:
            dest: tuple[int, int] = (drone.norm_x, drone.norm_y)
            self.graph_frame.blit(drone.get_sprite(direction), dest)

    def __place_sound(self, text: Surface) -> None:
        sound_coords: Coord = ((self.virtual_screen.get_width())
                               - text.get_width(), 0)
        self.graph_frame.blit(text, sound_coords)

    def __place_turn(self, text: Surface) -> None:
        turn_y: int = 0
        for hub in self.scenario.hubs:
            if (hub.norm_coord == (0, 0)):
                graph_h: int = self.graph_frame.get_height()
                text_h: int = text.get_height()
                turn_y = graph_h - text_h
                break
        self.graph_frame.blit(text, (0, turn_y))

    def __place_menu(self, text: Surface, direction: str) -> None:
        display.flip()
        menu: bool = True
        screen_w: int = self.virtual_screen.get_width()
        screen_h: int = self.virtual_screen.get_height()
        menu_w: int = self.menu.get_width()
        menu_h: int = self.menu.get_height()
        dest: Coord = (int(screen_w / 2 - menu_w / 2),
                       int(screen_h / 2 - menu_h / 2))
        while (menu):
            menu_img: Surface = image.load("src/menu.png")
            menu_img.set_colorkey((128, 64, 0))
            self.graph_frame.blit(self.bg_img)
            self.__place_connections()
            self.__place_hubs()
            self.__place_hub_names()
            self.__place_drones(direction)
            self.__place_sound(text)
            self.menu.blit(menu_img, (0, 0))
            self.graph_frame.blit(menu_img, dest)
            self.virtual_screen.blit(self.graph_frame, (0, 0))
            self.__resize()
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    exit(0)
                if (event.type == pygame.KEYDOWN):
                    if (event.key in [pygame.K_SPACE, pygame.K_ESCAPE]):
                        menu = False
            display.flip()

    def __move_drone(self, drone: Drone, hub: Hub) -> None:
        hub_size: int = drone.current_hub.sprite.get_height()
        hub_coord: Coord = (drone.current_hub.norm_coord[0],
                            drone.current_hub.norm_coord[1])
        new_coord: Coord = Adjuster.centralize_drone(hub_size,
                                                     drone.drone_size,
                                                     hub_coord)
        if ((drone.norm_x, drone.norm_y) != new_coord):
            norm_x: int = drone.norm_x
            norm_y: int = drone.norm_y
            new_x: int = new_coord[0]
            new_y: int = new_coord[1]
            var: Callable[[int, int,
                           int, int,
                           Coord], Coord] = Adjuster.variation_rate
            move_values: tuple[int, int] = var(norm_x,
                                               norm_y,
                                               new_x,
                                               new_y,
                                               hub.
                                               norm_coord)
            drone.move(move_values[0], move_values[1])

    def __resize(self) -> None:
        current_w: int = self.screen.get_width()
        current_h: int = self.screen.get_height()
        scaled: Surface = transform.scale(self.virtual_screen,
                                          (current_w, current_h))
        self.screen.blit(scaled)
