from typing import Callable
from .utils import Drone, Hub, HubError, Adjuster, Connection
from .Types import Hubs, Connecs, Path, Paths, Coord


class Scenario:
    def __init__(self: "Scenario",
                 nb_drones: int,
                 hubs: Hubs,
                 connections: Connecs) -> None:
        if (nb_drones <= 0):
            raise ValueError
        names: list[str] = [hub.name for hub in hubs]
        if (len(names) != len(set(names))):
            raise HubError("Hubs can't share the same name")
        coords: list[tuple[float, float]] = [hub.coordinates for hub in hubs]
        if (len(coords) != len(set(coords))):
            raise HubError("Hubs can't share the same coordinates")
        self.drones: list[Drone] = []
        self.hubs: Hubs = hubs
        self.connections: Connecs = connections
        for i in range(nb_drones):
            self.drones.append(Drone(self.get_start_hub(), f"D{i + 1}"))
        self.get_start_hub().total_drones = len(self.drones)
        self.phantom_hub()
        self.display_hubs()

    def phantom_hub(self: "Scenario") -> None:
        for i in range(len(self.hubs)):
            try:
                next_hub: Hub = self.hubs[i + 1]
                if ((next_hub.zone == "restricted") and (not (self.hubs[i].is_phantom))):
                    phantom_x: float = self.hubs[i].coordinates[0]
                    phantom_y: float = self.hubs[i].coordinates[1]
                    norm_x: int = self.hubs[i].norm_coord[0]
                    norm_y: int = self.hubs[i].norm_coord[1]
                    if (phantom_x < next_hub.coordinates[0]):
                        phantom_x += 0.5
                        norm_x = (int((next_hub.norm_coord[0] - self.hubs[i].norm_coord[0]) / 2)) + self.hubs[i].norm_coord[0]
                    elif (phantom_x > next_hub.coordinates[0]):
                        phantom_x -= 0.5
                        norm_x = (int((-next_hub.norm_coord[0] + self.hubs[i].norm_coord[0]) / 2)) + next_hub.norm_coord[0]
                    if (phantom_y < next_hub.coordinates[1]):
                        phantom_y += 0.5
                        norm_y = (int((next_hub.norm_coord[1] - self.hubs[i].norm_coord[1]) / 2)) + self.hubs[i].norm_coord[1]
                    elif (phantom_y > next_hub.coordinates[1]):
                        phantom_y -= 0.5
                        norm_y = (int((-next_hub.norm_coord[1] + self.hubs[i].norm_coord[1]) / 2)) + next_hub.norm_coord[1]
                    phantom: Hub = Hub(f"empty{i}",
                                        phantom_x,
                                        phantom_y,
                                        (next_hub.sprite.get_width(), next_hub.sprite.get_width()),
                                        {}, False,
                                        False,
                                        True)
                    phantom.set_handmade_norm_coord(norm_x, norm_y)
                    self.hubs.insert(i + 1, phantom)
                    for j in range(len(self.connections)):
                        if (self.connections[j].point1.name == self.hubs[j].name and self.connections[j].point2.name == next_hub.name):
                            connection1: Connection = Connection(phantom, self.hubs[j], self.connections[j].max_capacity)
                            connection2: Connection = Connection(next_hub, phantom, self.connections[j].max_capacity)
                            self.connections.pop(j)
                            self.connections.append(connection1)
                            self.connections.append(connection2)
            except IndexError:
                return

    def get_start_hub(self: "Scenario") -> Hub:
        ret: Hub = Hub("", 0, 0,
                       (0, 0), {},
                       False, False,
                       False)
        for hub in self.hubs:
            if (hub.is_start):
                ret = hub
        return (ret)

    def get_end_hub(self: "Scenario") -> Hub:
        ret: Hub = Hub("", 0, 0,
                       (0, 0), {},
                       False, False,
                       False)
        for hub in self.hubs:
            if (hub.is_end):
                ret = hub
        return (ret)

    def visitable_neighbours(self: "Scenario", hub: Hub | None) -> Hubs:
        if (hub is None):
            return ([])
        ret: Hubs = []
        for connection in self.connections:
            if ((connection.point1.name == hub.name) and
                    (connection.point1.zone != "blocked")):
                ret.append(connection.point2)
        return (ret)

    def verify_priority(self: "Scenario", hubs: Hubs) -> bool:
        for hub in hubs:
            if (hub.zone == "priority"):
                return (True)
        return (False)

    def solved_path(self: "Scenario") -> Paths:
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
            path += ([None] * i)
            path.reverse()
            ret.append(path)
            new_ret: Paths = []
            biggest_path_len: int = len(max(ret, key=len))
            for way in ret:
                new_way: Path = way
                if (len(new_way) < biggest_path_len):
                    new_way += [None] * (biggest_path_len - len(new_way))
                new_ret.append(new_way)
        return (new_ret)

    def display_hubs(self: "Scenario") -> None:
        for hub in self.hubs:
            print(f"{hub.name}, {hub.coordinates},"
                  f" (is_start: {hub.is_start}, is_end: {hub.is_end})",
                  f" norm_coords: {hub.norm_coord}")

    def display_connections(self: "Scenario") -> None:
        for connection in self.connections:
            print(f"{connection.point1.name}-{connection.point2.name}", end="")
            print(f" (max_capacity: {connection.max_capacity})")

    def stay_in_your_lane(self: "Scenario") -> bool:
        center: Callable[[int, int, Coord], Coord] = Adjuster.centralize_drone
        hub_size: int = self.hubs[0].sprite.get_width()
        drone_size: int = self.drones[0].drone_size
        for drone in self.drones:
            norm_coord: Coord = drone.current_hub.norm_coord
            if ((drone.norm_x, drone.norm_y) != center(hub_size,
                                                       drone_size,
                                                       norm_coord)):
                return (False)
        return (True)
