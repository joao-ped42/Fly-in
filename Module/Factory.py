from .utils import Parser, Adjuster
from .utils import FactoryError, HubSobrepositionError
from .Scenario import Scenario
from .Types import Hubs, Connecs, Filter


class Factory:
    @staticmethod
    def __get_nb_drones(lines: list[str]) -> int:
        for line in lines:
            if ((not (line.startswith("#"))) and (line != "\n")):
                if (line.split(":")[0] != "nb_drones"):
                    raise FactoryError("The first parameter of the file"
                                       " must be 'nb_drones'.")
                try:
                    return (int(line.split("#")[0].strip()
                                .split(":")[1].strip()))
                except ValueError:
                    raise FactoryError("'nb_drones' argument must be a"
                                       " number.")
        raise FactoryError("No 'nb_drones' was given")

    @staticmethod
    def __get_hubs(lines: list[str],
                   screen_w: int,
                   screen_h: int,
                   total_hubs: int) -> Hubs:
        ret: Hubs = []
        parser: Parser = Parser()
        graph_width: int = int(screen_w * (72.9 / 100))
        try:
            for line in lines:
                better_line: str = line.split("#")[0].strip()
                hub_type: str = better_line.split(":")[0].strip()
                parse_data: str = better_line.split(":")[1].strip()
                if (hub_type == 'start_hub'):
                    ret.append(parser.get_hub(parse_data,
                                              graph_width,
                                              total_hubs,
                                              True, False))
                elif (hub_type == 'end_hub'):
                    ret.append(parser.get_hub(parse_data,
                                              graph_width,
                                              total_hubs,
                                              False, True))
                else:
                    ret.append(parser.get_hub(parse_data,
                                              graph_width,
                                              total_hubs,
                                              False, False))
        except Exception as e:
            raise FactoryError(f"{e}")
        coords: list[tuple[int, int]] = []
        for hub in ret:
            coords.append(hub.coordinates)
        hubs_x: list[int] = [x for x, _ in coords]
        hubs_y: list[int] = [y for _, y in coords]
        max_xy: tuple[int, int] = (max(hubs_x), max(hubs_y))
        min_xy: tuple[int, int] = (min(hubs_x), min(hubs_y))
        img_size: int = Adjuster.size_adjuster(894, graph_width, total_hubs)
        screen_info: tuple[int, int] = (graph_width - img_size,
                                        int(screen_h - (img_size)))
        for hub in ret:
            hub.set_norm_coord(min_xy,
                               max_xy,
                               screen_info[0],
                               screen_info[1])
        return (ret)

    @staticmethod
    def __get_connecs(lines: list[str], hubs: Hubs) -> Connecs:
        ret: Connecs = []
        parser: Parser = Parser()
        try:
            for line in lines:
                parse_data: str = line.split(":")[1].strip()
                ret.append(parser.get_connection(parse_data, hubs))
        except Exception as e:
            raise FactoryError(f"{e}")
        return (ret)

    def read_file(self, file_name: str,
                  screen_w: int,
                  screen_h: int) -> Scenario:
        with open(file_name, "r") as file:
            lines: list[str] = file.readlines()
        Parser.Validator.verify_config_file(lines)
        try:
            hub_types: tuple[str, str, str] = ("hub:",
                                               "start_hub:",
                                               "end_hub:")
            hub_filter: Filter = lambda x: x.startswith(hub_types)
            connec_filter: Filter = lambda x: x.startswith("connection:")

            hubs_data: list[str] = list(filter(hub_filter, lines))
            connecs_data: list[str] = list(filter(connec_filter, lines))

            if (sum([1 for string in hubs_data
                     if string.startswith("start_hub")]) != 1):
                raise HubSobrepositionError("start_hub quantity "
                                            "is different than 1")
            if (sum([1 for string in hubs_data
                     if string.startswith("end_hub")]) != 1):
                raise HubSobrepositionError("end_hub quantity"
                                            " is different than 1")

            nb_drones: int = self.__get_nb_drones(lines)
            hubs: Hubs = self.__get_hubs(hubs_data,
                                         screen_w,
                                         screen_h,
                                         len(hubs_data))
            connections: Connecs = self.__get_connecs(connecs_data, hubs)
        except Exception as e:
            raise FactoryError(f"Error parsing data: {e}")
        return (Scenario(nb_drones, hubs, connections))
