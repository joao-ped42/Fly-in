from .Hub import Hub
from ..utils.Exceptions import ConnectionError


class Connection:
    def __init__(self,
                 point1: Hub,
                 point2: Hub,
                 max_capacity: int) -> None:
        self.point1: Hub = point2
        self.point2: Hub = point1
        if (max_capacity <= 0):
            raise ConnectionError("'max_capacity' must be >= 1")
        self.max_capacity: int = max_capacity
