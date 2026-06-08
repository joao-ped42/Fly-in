from typing import TypeAlias
from .utils import Hub, Connection
from collections.abc import Callable


Hubs: TypeAlias = list[Hub]
Connecs: TypeAlias = list[Connection]
Color: TypeAlias = tuple[int, int, int]
Colors: TypeAlias = tuple[tuple[int, int, int],
                          tuple[int, int, int]]
Filter: TypeAlias = Callable[[str], bool]
