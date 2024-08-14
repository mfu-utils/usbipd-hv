from src.FilterMode import FilterMode


class DeviceFilter:
    def __init__(self, name: str, filter_by: str, value: str, mode: FilterMode, force: bool):
        self.__filter_by = filter_by
        self.__value = value
        self.__mode = mode
        self.__force = force
        self.__name = name

    def name(self) -> str:
        return self.__name

    def filter_by(self) -> str:
        return self.__filter_by

    def value(self) -> str:
        return self.__value

    def mode(self) -> FilterMode:
        return self.__mode

    def force(self) -> bool:
        return self.__force
