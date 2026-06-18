from .utils import Hub, Connection
from typing import TypeAlias
from collections.abc import Callable


Hubs: TypeAlias = list[Hub]
Coord: TypeAlias = tuple[int, int]
Connecs: TypeAlias = list[Connection]
Color: TypeAlias = tuple[int, int, int]
Filter: TypeAlias = Callable[[str], bool]
Coords: TypeAlias = list[tuple[int, int]]
Colors: TypeAlias = tuple[tuple[int, int, int],
                          tuple[int, int, int]]
Path: TypeAlias = list[tuple[tuple[int, int], Hub]]
