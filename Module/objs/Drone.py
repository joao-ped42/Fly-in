from .Hub import Hub
from ..utils.Adjuster import Adjuster
from random import choice
import os
from pygame import Surface, image, transform


class Drone:
    def __init__(self, hub: Hub, drone_id: str) -> None:
        self.sprite_index: float = 0
        self.drone_id: str = drone_id
        self.current_hub: Hub = hub
        self.sprite_list: list[str] = self.__get_sprites()
        hub_size: int = hub.sprite.get_width()
        self.drone_size: int = int(hub_size * 4/5)
        self.norm_x: int = Adjuster.centralize_drone(hub_size,
                                                     self.drone_size,
                                                     (hub.norm_coord[0],
                                                      hub.norm_coord[1]))[0]
        self.norm_y: int = Adjuster.centralize_drone(hub_size,
                                                     self.drone_size,
                                                     (hub.norm_coord[0],
                                                      hub.norm_coord[1]))[1]
        self.waiting: bool = True
        self.sol_index: int = 0

    def get_sprite(self, direction: str) -> Surface:
        i: int = int(self.sprite_index)
        sprites_len: int = len(self.sprite_list)
        img: Surface = image.load(self.sprite_list[i % (sprites_len - 1)])
        resize: Surface = transform.scale(img, (self.drone_size,
                                                self.drone_size))
        self.sprite_index += 0.7
        if (self.pokemon != 'sonic/shiny' and direction == "right"):
            ret: Surface = transform.flip(resize, True, False)
            return (ret)
        return (resize)

    def move(self, plus_x: int, plus_y: int) -> None:
        hub_size: int = self.current_hub.sprite.get_width()
        hub_coords: tuple[int, int] = (self.current_hub.norm_coord[0],
                                       self.current_hub.norm_coord[1])
        img_size: int = self.drone_size
        new_coord: tuple[int, int] = Adjuster.centralize_drone(hub_size,
                                                               img_size,
                                                               hub_coords)
        if (plus_x >= 0 and self.norm_x + plus_x > new_coord[0]):
            plus_x = new_coord[0] - self.norm_x
            # print("plus_x =", plus_x)
            # print("plus_y =", plus_y)
        if (plus_y >= 0 and self.norm_y + plus_y > new_coord[1]):
            plus_y = new_coord[1] - self.norm_y
        elif ((plus_x != 0) and
              (self.norm_x + plus_x == new_coord[0]) and
              (self.norm_y + plus_y != new_coord[1])):
            if (new_coord[1] > self.norm_y):
                plus_y = (new_coord[1] - self.norm_y)
            else:
                plus_y = (-self.norm_y + new_coord[1])
        self.norm_x += plus_x
        self.norm_y += plus_y

    def move_to_hub(self, new_hub: Hub) -> None:
        if (self.current_hub != new_hub):
            self.current_hub = new_hub
        if ((not (new_hub.is_start)) and (self.waiting)):
            self.waiting = False
        # elif ((new_hub.is_end) and (not (self.waiting))):
        #     self.waiting = True

    def __get_sprites(self) -> list[str]:
        sprites: list[str] = ["abra",
                              "aerodactyl",
                              "archeops",
                              "bombirdier",
                              "butterfree",
                              "carnivine",
                              "clefable",
                              "crobat",
                              "dragonite",
                              "haunter",
                              "mismagius",
                              "quaquaval",
                              "sonic"]
        sprite_list: list[str] = []
        self.pokemon: str = choice(sprites)
        if ((self.pokemon not in ['clefable',
                                  'bombirdier',
                                  'dragonite']) and
                choice(range(4096)) == 67):
            self.pokemon += '/shiny'
        folder: str = f"src/drones/{self.pokemon}"
        for sprite in os.listdir(folder):
            full_path: str = os.path.join(folder, sprite)
            if os.path.isfile(full_path):
                sprite_list.append(f"{folder}/{sprite}")
        return (list(sorted(sprite_list)))
