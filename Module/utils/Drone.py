from pygame import Surface, image
from .Hub import Hub
from random import choice


class Drone:
    def __init__(self, hub: Hub, drone_id: str) -> None:
        sprites: list[str] = ["aerodactyl",
                              "dr_robotnik",
                              "jumpluff",
                              "latios",
                              "scyther"]
        self.sprite: Surface = image.load(f"src/drones/{choice(sprites)}.png")
        self.current_hub: Hub = hub
        self.norm_x: int = hub.norm_coord[0]
        self.norm_y: int = hub.norm_coord[1]
