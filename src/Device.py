from src.DeviceStatus import DeviceStatus


class Device:
    def __init__(self, bus_id: str, vid: str, pid: str, name: str, state: DeviceStatus):
        self.__bus_id = bus_id
        self.__vid = vid
        self.__pid = pid
        self.__name = name
        self.__state = state

    def bus_id(self) -> str:
        return self.__bus_id

    def vid(self) -> str:
        return self.__vid

    def pid(self) -> str:
        return self.__pid

    def name(self) -> str:
        return self.__name

    def state(self) -> DeviceStatus:
        return self.__state

    def __repr__(self) -> str:
        data = [self.__bus_id, self.__name]

        return f'<Device ({":".join(data)})>'
