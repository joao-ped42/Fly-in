from .utils import Hub, Connection
from typing import TypeAlias
from collections.abc import Callable


Hubs: TypeAlias = list[Hub]
Path: TypeAlias = list[Hub | None]
Coord: TypeAlias = tuple[int, int]
Connecs: TypeAlias = list[Connection]
Color: TypeAlias = tuple[int, int, int]
Filter: TypeAlias = Callable[[str], bool]

Paths: TypeAlias = list[Path]
Coords: TypeAlias = list[Coord]
Colors: TypeAlias = tuple[Color, Color]
