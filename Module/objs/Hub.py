from ..utils.Adjuster import Adjuster
from ..utils.Exceptions import HubSobrepositionError, IndexControl
from pygame import Surface
from pygame.image import load
from pygame.transform import scale


class Hub:
    def __init__(self: "Hub",
                 name: str,
                 x: float, y: float,
                 sprite_size: tuple[int, int],
                 metadata: dict[str, str | int],
                 is_start: bool,
                 is_end: bool,
                 is_phantom: bool) -> None:
        if (is_start and is_end):
            raise HubSobrepositionError(
                "Start and goal can't have the same coordinates"
                )
        self.name: str = name
        self.coordinates: tuple[float, float] = (x, y * (-1))
        self.zone: str = "normal"
        self.max_drones: int = 1
        img: Surface = load("src/hubs/rainbow.png")
        if ("color" in metadata):
            img = load(f"src/hubs/{metadata['color']}.png")
        self.sprite: Surface = scale(img, (sprite_size[0], sprite_size[1]))
        if ("zone" in metadata):
            if (isinstance(metadata['zone'], str)):
                self.zone = metadata['zone']
        if ("max_drones" in metadata):
            if (isinstance(metadata['max_drones'], int)):
                self.max_drones = metadata['max_drones']
        self.is_start: bool = is_start
        self.is_end: bool = is_end
        if (self.is_end):
            end_effect: Surface = load("src/hubs/spark.png")
            resized_end_effect: Surface = scale(end_effect,
                                                (self.sprite.get_width(),
                                                 self.sprite.get_width()))
            self.sprite.blit(resized_end_effect, (0, 0))
        self.is_visited: bool = False
        self.total_drones: int = 0
        self.is_phantom: bool = is_phantom
        if (is_phantom):
            print("criei fantasma")

    def deport_drone(self: "Hub") -> None:
        if (self.total_drones != 0):
            self.total_drones -= 1

    def repatriate_drone(self: "Hub") -> None:
        if (self.total_drones == self.max_drones):
            raise IndexControl
        self.total_drones += 1

    def set_norm_coord(self: "Hub",
                       min_xy: tuple[float, float],
                       max_xy: tuple[float, float],
                       screen_w: int, screen_h: int) -> None:
        a: Adjuster = Adjuster()
        min_x: float = min_xy[0]
        max_x: float = max_xy[0]
        min_y: float = min_xy[1]
        max_y: float = max_xy[1]
        self.norm_coord: tuple[int, int] = a.normalize_coord(self.coordinates,
                                                             min_x, max_x,
                                                             min_y, max_y,
                                                             screen_w,
                                                             screen_h)

    def set_handmade_norm_coord(self: "Hub",
                                norm_x: int,
                                norm_y: int) -> None:
        self.norm_coord = (norm_x, norm_y)
