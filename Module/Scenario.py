from .utils import Drone, Hub, HubError
from .Types import Hubs, Connecs, Path, Paths


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
        coords: list[tuple[int, int]] = [hub.coordinates for hub in hubs]
        if (len(coords) != len(set(coords))):
            raise HubError("Hubs can't share the same coordinates")
        self.drones: list[Drone] = []
        self.hubs: Hubs = hubs
        self.connections: Connecs = connections
        for i in range(nb_drones):
            self.drones.append(Drone(self.get_start_hub(), f"D{i + 1}"))

    def get_start_hub(self) -> Hub:
        ret: Hub = Hub("", 0, 0,
                       (0, 0), {},
                       False, False)
        for hub in self.hubs:
            if (hub.is_start):
                ret = hub
        return (ret)

    def get_end_hub(self) -> Hub:
        ret: Hub = Hub("", 0, 0,
                       (0, 0), {},
                       False, False)
        for hub in self.hubs:
            if (hub.is_end):
                ret = hub
        return (ret)

    def visitable_neighbours(self, hub: Hub | None) -> Hubs:
        if (hub is None):
            return ([])
        ret: Hubs = []
        for connection in self.connections:
            if ((connection.point1.name == hub.name) and
                    (connection.point1.zone != "blocked")):
                ret.append(connection.point2)
            # elif ((connection.point2.name == hub.name) and
            #         (connection.point2.zone != "blocked")):
            #     ret.append(connection.point1)
        return (ret)

    def verify_priority(self, hubs: Hubs) -> bool:
        for hub in hubs:
            if (hub.zone == "priority"):
                return (True)
        return (False)

    def solved_path(self) -> Paths:
        start: Hub = self.get_start_hub()
        end: Hub = self.get_end_hub()
        queue: Hubs = [start]
        visited: set[Hub] = {start}
        previous: dict[Hub, Hub | None] = {start: None}

        while (queue):
            current_hub: Hub | None = queue.pop(0)
            if (current_hub == end):
                break
            neighbors: Hubs = self.visitable_neighbours(current_hub)
            # for neighbor in neighbors:
            #     for drone in self.drones:
            #         if (drone.current_hub == neighbor):
            for neighbor in neighbors:
                if (self.verify_priority(neighbors) and
                        neighbor.zone != "priority"):
                    continue
                if (neighbor in visited):
                    continue
                visited.add(neighbor)
                previous[neighbor] = current_hub
                queue.append(neighbor)

        if (end not in previous):
            return ([])
        ret: Paths = []
        for i in range(len(self.drones)):
            path: Path = []
            current_hub = end
            while (current_hub is not None):
                path.append(current_hub)
                current_hub = previous[current_hub]
            path = ([None] * i) + path + ([None] * i)
            path.reverse()
            # for hub in path:
            #     if hub == None:
            #         print("hub.name = None ", end="")
            #     else:
            #         print("hub.name =", hub.name, " ", end="")
            # print()
            # print(f"=================={i}=================")
            # if ((not (path)) or (path[0][1] != start)):
            #     return ([])
            ret.append(path)
            # for path in ret:
        return (ret)

    def display_hubs(self) -> None:
        for hub in self.hubs:
            print(f"{hub.name}, {hub.coordinates},"
                  f" (is_start: {hub.is_start}, is_end: {hub.is_end})")

    def display_connections(self) -> None:
        for connection in self.connections:
            print(f"{connection.point1.name}-{connection.point2.name}", end="")
            print(f" (max_capacity: {connection.max_capacity})")
