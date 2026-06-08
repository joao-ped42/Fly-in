from pygame import Surface, image
from .Hub import Hub
from random import choice


class Drone:
    def __init__(self, hub: Hub, drone_id: str) -> None:
        self.drone_id: str = drone_id
        self.current_hub: Hub = hub
        self.norm_x: int = hub.norm_coord[0]
        self.norm_y: int = hub.norm_coord[1]
        sprites: list[str] = ["abra",
                              "aerodactyl",
                              "beedrill",
                              "butterfree",
                              "dr_robotnik",
                              "gastly",
                              "gligar",
                              "haunter",
                              "ho-oh",
                              "jumpluff",
                              "latios",
                              "ledian",
                              "magneton",
                              "misdreavous",
                              "porygon",
                              "scyther",
                              "zubat"]
        self.sprite: Surface = image.load(f"src/drones/{choice(sprites)}.png")
        print(self.norm_x, self.norm_y)

    def move(self, plus_x: int, plus_y: int) -> None:
        if (self.norm_x + plus_x > self.current_hub.norm_coord[0]):
            plus_x = self.current_hub.norm_coord[0] - self.norm_x
        if (self.norm_y + plus_y > self.current_hub.norm_coord[1]):
            plus_y = self.current_hub.norm_coord[1] - self.norm_y
        self.norm_x += plus_x
        self.norm_y += plus_y

    def move_to_hub(self, new_hub: Hub) -> None:
        self.current_hub = new_hub
