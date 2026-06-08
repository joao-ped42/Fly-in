from .Hub import Hub
from .Connection import Connection
from .Exceptions import ConnectionError, MetadataError
from .Adjuster import Adjuster


class Parser:
    class Validator:
        @staticmethod
        def verify_config_file(lines: list[str]) -> None:
            line_num: int = 1
            for line in lines:
                if ((not (line.strip().startswith("#")))
                        and (not (line.isspace()))):
                    line_split: list[str] = line.split(":")
                    if (len(line_split) == 1):
                        print(f"Line {line_num} is invalid,",
                              "if something goes wrong, maybe that's why.")
                    else:
                        if (line_split[0].strip() not in ['hub',
                                                          'start_hub',
                                                          'end_hub',
                                                          'connection',
                                                          'nb_drones']):
                            print(f"Line {line_num} is invalid,",
                                  "if something goes wrong, maybe that's why.")
                line_num += 1

        @staticmethod
        def metadaticfy(data: list[str], index: int) -> str:
            metadata: str = ""
            while (index < len(data)):
                for char in data[index]:
                    if (char not in "[]"):
                        metadata += char
                metadata += " "
                index += 1
            return (metadata.strip())

        @staticmethod
        def validate_metadata(data: str) -> bool:
            data_split: list[str] = data.split(" ")
            i: int = 0
            while (i < len(data_split)):
                prefix: str = data_split[i].split("=")[0]
                value: str = data_split[i].split("=")[1]
                if (prefix == 'zone'):
                    if (value not in ['normal', 'blocked',
                                      'restricted', 'priority']):
                        return (False)
                elif (prefix == 'color'):
                    if (not (value.isalpha())):
                        return (False)
                elif (prefix == "max_drones" or prefix == "max_link_capacity"):
                    if (not (value.isdigit())):
                        return (False)
                else:
                    return (False)
                i += 1
            return (True)

        def validate_hub(self, hub_data: str) -> bool:
            hub_data_split: list[str] = hub_data.split(" ")
            if ('-' in hub_data_split[0]):
                return (False)
            try:
                int(hub_data_split[1])
                int(hub_data_split[2])
            except ValueError:
                return (False)
            if (len(hub_data_split) > 3):
                metadata: str = self.metadaticfy(hub_data_split, 3)
                if (not (self.validate_metadata(metadata))):
                    return (False)
            return (True)

    def get_connection(self, con_data: str, hubs: list[Hub]) -> Connection:
        con_data_split: list[str] = con_data.split(" ")
        hub1_name: str = con_data_split[0].split('-')[0]
        hub2_name: str = con_data_split[0].split('-')[1]
        parent: Hub = Hub("", 0, 0, (0, 0),
                          {"color": "red"}, False, False)
        child: Hub = Hub("", 0, 0, (0, 0),
                         {"color": "red"}, False, False)
        for hub in hubs:
            if (hub.name == hub1_name):
                child = hub
            if (hub.name == hub2_name):
                parent = hub
        if ((child.name == "") or (parent.name == "")):
            raise ConnectionError("Invalid Connection")
        max_capacity: int = 1
        if (len(con_data_split) > 1):
            max_capacity_data: str\
                = self.Validator.metadaticfy(con_data_split, 1)
            try:
                max_capacity = int(max_capacity_data.split("=")[1])
            except ValueError:
                raise ConnectionError("'max_capacity' must recieve"
                                      " an integer.")
        return (Connection(parent, child, max_capacity))

    def get_hub(self, hub_data: str,
                graph_w: int,
                total_hubs: int,
                is_start: bool,
                is_end: bool) -> Hub:

        if (self.Validator().validate_hub(hub_data)):
            hub_data_split: list[str] = hub_data.split(" ")
            name: str = hub_data_split[0]
            x: int = int(hub_data_split[1])
            y: int = int(hub_data_split[2])
            img_size: int = Adjuster.size_adjuster(894, graph_w, total_hubs)
            metadata: dict[str, str | int] = {"color": "None"}
            if (len(hub_data_split) > 3):
                base_metadata: str = self.Validator.metadaticfy(hub_data_split,
                                                                3)
                metadata = self.get_metadata(base_metadata)
            return (Hub(name,
                        x, y,
                        (img_size, img_size),
                        metadata,
                        is_start,
                        is_end))
        else:
            raise ValueError("Invalid data")

    def get_metadata(self, data: str) -> dict[str, str | int]:
        if (self.Validator.validate_metadata(data)):
            metadatas: list[str] = data.split(" ")
            ret: dict[str, str | int] = {}
            for m_data in metadatas:
                dict_key: str = m_data.split("=")[0]
                dict_val: str = m_data.split("=")[1]
                if (dict_val.isdigit()):
                    ret.update({dict_key: int(dict_val)})
                else:
                    ret.update({dict_key: dict_val})
            return (ret)
        else:
            raise MetadataError("Invalid metadata")
