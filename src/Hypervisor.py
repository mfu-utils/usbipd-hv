import os.path
import re
from enum import Enum
from typing import List, Tuple, Optional

from src.Device import Device
from src.DeviceStatus import DeviceStatus
from src.Ini import Ini
import subprocess

from src.Log import Log
from src.Utils.Filters import Filters


def run(parameters: List[str]) -> Tuple[int, str]:
    process = subprocess.run(parameters, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return_code = process.returncode
    out = (process.stdout if return_code == 0 else process.stderr).decode('utf-8')

    return return_code, out


class Hypervisor:
    USBIPD = 'usbipd'
    LIST = [USBIPD, 'list']
    BIND = [USBIPD, 'bind', '--busid']
    UNBIND = [USBIPD, 'unbind', '--busid']
    ATTACH = [USBIPD, 'attach', '--wsl', '--busid']
    DETACH = [USBIPD, 'detach', '--busid']

    EMPTY = re.compile(r"\s\s+")

    class FilterMode(Enum):
        Like = 'like'
        Regex = 'regex'
        Key = 'key'

    def __init__(self, ini: Ini, log: Log):
        self.__ini = ini
        self.__log = log

    def determinate_filter_mode(self, value: str) -> Optional[FilterMode]:
        try:
            return Hypervisor.FilterMode(value)
        except ValueError:
            self.__log.error(f"Cannot determine filter mode ({value}).")

    def usb_ipd_filter(self, devices: List[Device], parameter: str, _filter: str, mode: FilterMode) -> List[Device]:
        filtered = []

        for device in devices:
            try:
                value = device.__getattribute__(parameter)
            except AttributeError:
                self.__log.error(f"Parameter {parameter} not found.")
                return []

            if mode == Hypervisor.FilterMode.Key:
                if not Filters.filter_key(value, _filter):
                    continue
            elif mode == Hypervisor.FilterMode.Regex:
                regex = Filters.create_regex_filter(_filter, self.__log)

                if not Filters.filter_regex(value, regex):
                    continue
            elif mode == Hypervisor.FilterMode.Like:
                if not Filters.filter_like(value, _filter):
                    continue

            filtered.append(device)

        return filtered

    def usb_ipd_bind(self, device: Device) -> bool:
        code, out = run([*self.BIND, device.bus_id()])

        if code > 0:
            self.__log.error(f'USB IPD bind failed: {out}')
            return False

        return True

    def usb_ipd_list(self) -> List[Device]:
        code, out = run(self.LIST)

        if code > 0:
            self.__log.error(f"Cannot get usbipd list. {out}")
            return []

        lines = out.split(os.linesep)

        devices = []

        for line in lines[2:]:
            if not line:
                break

            params = self.EMPTY.split(line)
            vid, pid = params[1].split(':')
            devices.append(Device(params[0], vid, pid, params[2], DeviceStatus(params[3])))

        return devices
