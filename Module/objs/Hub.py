from ..utils.Adjuster import Adjuster
from ..utils.Exceptions import HubSobrepositionError
from pygame import Surface
from pygame.image import load
from pygame.transform import scale


class Hub:
    def __init__(self, name: str,
                 x: int, y: int,
                 sprite_size: tuple[int, int],
                 metadata: dict[str, str | int],
                 is_start: bool,
                 is_end: bool) -> None:
        if (is_start and is_end):
            raise HubSobrepositionError(
                "Start and goal can't have the same coordinates"
                )
        self.name: str = name
        self.coordinates: tuple[int, int] = (x, y * (-1))
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

    def set_norm_coord(self, min_xy: tuple[int, int],
                       max_xy: tuple[int, int],
                       screen_w: int, screen_h: int) -> None:
        a: Adjuster = Adjuster()
        min_x: int = min_xy[0]
        max_x: int = max_xy[0]
        min_y: int = min_xy[1]
        max_y: int = max_xy[1]
        self.norm_coord: tuple[int, int] = a.normalize_coord(self.coordinates,
                                                             min_x, max_x,
                                                             min_y, max_y,
                                                             screen_w,
                                                             screen_h)
