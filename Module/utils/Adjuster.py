from math import exp


class Adjuster:
    def normalize_coord(self,
                        coord: tuple[int, int],
                        min_x: int, max_x: int,
                        min_y: int, max_y: int,
                        screen_w: int,
                        screen_h: int) -> tuple[int, int]:

        graph_w: int = max_x - min_x
        graph_h: int = max_y - min_y
        if (graph_w == 0):
            graph_w = 1
        if (graph_h == 0):
            graph_h = 1
        scale_x: float = screen_w / graph_w
        scale_y: float = screen_h / graph_h
        scale_y = min(scale_x, scale_y)
        graph_center_x: float = ((max_x + min_x) / 2)
        graph_center_y: float = (max_y + min_y) / 2
        screen_center_x: float = screen_w / 2
        screen_center_y: float = screen_h / 2
        screen_x: int = int((coord[0] - graph_center_x)
                            * scale_x + screen_center_x)
        screen_y: int = int((coord[1] - graph_center_y)
                            * scale_y + screen_center_y)
        return (int(screen_x), int(screen_y))

    @staticmethod
    def size_adjuster(image_w: int, surface_w: int, total_hubs: int) -> int:
        def f(x: int) -> float:
            return (300 * (1 - exp(-0.45 * x)))
        var: float = ((surface_w - (total_hubs - 1))
                      / (total_hubs * (image_w + f(total_hubs))))
        if (var * image_w) < 50:
            return 50
        return (int((image_w * var)))

    @staticmethod
    def variation_rate(current_x: int,
                       current_y: int,
                       next_x: int,
                       next_y: int) -> tuple[int, int]:
        delta_x: int = next_x - current_x
        delta_y: int = next_y - current_y
        vel: float = 35
        if (delta_x != 0 and delta_y != 0):
            delta: float = (delta_y / delta_x)
            ret_y: float = vel * delta
            if (delta_x < 0):
                return ((int(-vel), int(-ret_y)))
            return ((int(vel), int(ret_y)))
        if (delta_x == 0):
            if (delta_y < 0):
                return ((0, int(-vel)))
            return ((0, int(vel)))
        if (delta_y == 0):
            if (delta_x < 0):
                return ((int(-vel), 0))
            return ((int(vel), 0))
        return ((0, 0))

    @staticmethod
    def centralize_drone(hub_size: int,
                         drone_size: int,
                         hub_coords: tuple[int, int]) -> tuple[int, int]:
        hub_x: int = hub_coords[0]
        hub_y: int = hub_coords[1]
        ret_x: int = hub_x + (int(hub_size / 2)) - (int(drone_size / 2))
        ret_y: int = hub_y + (int(hub_size / 2)) - (int(drone_size / 2))
        return (int(ret_x), int(ret_y))
