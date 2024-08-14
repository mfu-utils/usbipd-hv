from typing import List

from src.DeviceStatus import DeviceStatus


class Device:
    def __init__(self, bus_id: str, vid: str, pid: str, description: str, state: DeviceStatus):
        self.__bus_id = bus_id
        self.__vid = vid
        self.__pid = pid
        self.__description = description
        self.__state = state

    def bus_id(self) -> str:
        return self.__bus_id

    def vid(self) -> str:
        return self.__vid

    def pid(self) -> str:
        return self.__pid

    def description(self) -> str:
        return self.__description

    def state(self) -> DeviceStatus:
        return self.__state

    @staticmethod
    def get_available_parameters_list() -> List[str]:
        return ["bus_id", "vid", "pid", "description"]

    def __repr__(self) -> str:
        data = [self.__bus_id, self.__description]

        return f'Device({", ".join(data)})'
