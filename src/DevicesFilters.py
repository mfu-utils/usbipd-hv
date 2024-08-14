import os

import yaml
from typing import Optional, List, Tuple

from config import CWD
from src.Device import Device
from src.DeviceFilter import DeviceFilter
from src.FilterMode import FilterMode
from src.Log import Log


class DevicesFilters:
    def __init__(self, path: str, log: Log):
        self.__log = log
        self.__success_loaded = False

        self.__path = path

        if not os.path.isabs(self.__path):
            self.__path = os.path.join(CWD, self.__path)

        try:
            with open(self.__path, 'r') as f:
                self.__data = yaml.load(f, yaml.SafeLoader)
                self.__success_loaded = True
        except FileNotFoundError:
            self.__log.error(f"Cannot get filter file ({self.__path}).")
            return

        self.__validators = [
            self.__validate_filter_by,
            self.__validate_value,
            self.__validate_mode,
            self.__validate_force,
        ]

    def success_loaded(self) -> bool:
        return self.__success_loaded

    @staticmethod
    def __wrap_message(filter_name: str, message: str) -> str:
        return f"Filter '{filter_name}':: {message}"

    @staticmethod
    def __validate_value(_filter: dict) -> Optional[str]:
        if not (value := _filter.get('value')):
            return f"Missing 'value' parameter."

        if not isinstance(value, str):
            return f"'value' parameter must be a string."

    @staticmethod
    def __validate_mode(_filter: dict) -> Optional[str]:
        if not (mode := _filter.get('mode')):
            return f"Missing 'mode' parameter."

        if not isinstance(mode, str):
            return f"'mode' parameter must be a string."

        modes = list(map(lambda x: x.name, FilterMode))

        if mode not in modes:
            modes = ", ".join(modes)
            return f"'mode' parameter is not a valid. Please use [{modes}]"

    @staticmethod
    def __validate_force(_filter: dict) -> Optional[str]:
        if not (force := _filter.get('force')):
            return

        if not isinstance(force, bool):
            return f"'force' must be a boolean type."

    @staticmethod
    def __validate_filter_by(_filter: dict) -> Optional[str]:
        if not (filter_by := _filter.get('filter_by')):
            return f"Missing 'filter_by' parameter."

        if not isinstance(filter_by, str):
            return f"'filter_by' parameter must be a string."

        if filter_by not in Device.get_available_parameters_list():
            params = ', '.join(Device.get_available_parameters_list())
            return f"'filter_by' is not available parameter. Please use [{params}]."

        return None

    def create_filters(self) -> Tuple[bool, List[DeviceFilter]]:
        if not isinstance(self.__data, dict):
            self.__log.error('Cannot create filters without a dictionary.')
            return False, []

        devices_filters: List[DeviceFilter] = []

        for name, data in self.__data.items():
            if not self.__validate_filter(name, data):
                return False, []

            devices_filters.append(DeviceFilter(
                name,
                data['filter_by'],
                data['value'],
                FilterMode[data['mode']],
                data.get('force') or False
            ))

        return True, devices_filters

    def __validate_filter(self, _filter_name: str, _filter: dict) -> bool:
        for validator in self.__validators:
            if message := validator(_filter):
                self.__log.error(self.__wrap_message(_filter_name, message))
                return False

        return True
