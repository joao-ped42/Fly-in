from .utils import Drone, Hub, HubError
from .Types import Hubs, Connecs


class Scenario:
    def __init__(self,
                 nb_drones: int,
                 hubs: Hubs,
                 connections: Connecs) -> None:
        if (nb_drones <= 0):
            raise ValueError
        names: list[str] = [hub.name for hub in hubs]
        if (len(names) != len(set(names))):
            raise HubError("Hubs can't share the same name")
        self.drones: list[Drone] = []
        self.hubs: Hubs = hubs
        self.connections: Connecs = connections
        for i in range(nb_drones):
            self.drones.append(Drone(self.get_start_hub(), f"D{i + 1}"))

    def get_start_hub(self) -> Hub:
        ret: Hub = Hub("", 0, 0,
                       (0, 0), {}, False, False)
        for hub in self.hubs:
            if (hub.is_start):
                ret = hub
        return (ret)

    def display_hubs(self) -> None:
        for hub in self.hubs:
            print(f"{hub.name}, {hub.coordinates},"
                  f" (is_start: {hub.is_start}, is_end: {hub.is_end})")

    def display_connections(self) -> None:
        for connection in self.connections:
            print(f"{connection.point1.name}-{connection.point2.name}", end="")
            print(f" (max_capacity: {connection.max_capacity})")
