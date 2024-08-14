import subprocess
import os.path
import re

from typing import List, Tuple
from time import sleep
from sys import exit

from src.DevicesFilters import DevicesFilters
from src.DeviceStatus import DeviceStatus
from src.FilterMode import FilterMode
from src.Utils.Filters import Filters
from src.Device import Device
from src.Ini import Ini
from src.Log import Log


def run(parameters: List[str]) -> Tuple[int, str]:
    process = subprocess.run(parameters, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return_code = process.returncode
    out = (process.stdout if return_code == 0 else process.stderr).decode('utf-8')

    return return_code, out.strip()


class Hypervisor:
    _USBIPD = 'usbipd'
    _FORCE = '--force'
    CMD_LIST = [_USBIPD, 'list']
    CMD_BIND = [_USBIPD, 'bind', '--busid']
    CMD_ATTACH = [_USBIPD, 'attach', '--wsl', '--busid']

    # CMD_UNBIND = [_USBIPD, 'unbind', '--busid']
    # CMD_DETACH = [_USBIPD, 'detach', '--busid']

    EMPTY = re.compile(r"\s\s+")

    def __init__(self, ini: Ini, log: Log):
        self.__ini = ini
        self.__log = log

        try:
            self.__timeout = self.__ini.get('app.timeout', int)
        except BaseException as e:
            self.__log.error(f'Cannot get app.timeout. {str(e)}')
            return

        if self.__timeout < 0:
            self.__log.error(f'app.timeout cannot be less than 0.')
            return

        if not (device_filter_path := self.__ini.get('filters.path')):
            self.__log.error("filters.path not found in ini file")
            return

        if not os.path.exists(device_filter_path):
            self.__log.error(f"Filters file not found at '{device_filter_path}'")

        filters_service = DevicesFilters(device_filter_path, self.__log)

        if not filters_service.success_loaded():
            return

        ok, self.__devices_filters = filters_service.create_filters()

        if not ok:
            self.__log.error("Failed to create filters.")
            return

        try:
            self.__run()
        except KeyboardInterrupt:
            self.__log.warning("Keyboard interrupt received. Stopping.")

    def __usb_ipd_filter(self, devices: List[Device], filter_by: str, _filter: str, mode: FilterMode) -> List[Device]:
        self.__log.debug("Try filtering usbipd devices")
        filtered = []

        for device in devices:
            if device.state() == DeviceStatus.Attached:
                self.__log.debug(f"Skip device ({device}). Has been attached.")
                continue

            value = device.__getattribute__(filter_by)()

            skip = False

            if mode == FilterMode.Key:
                if not Filters.filter_key(value, _filter):
                    skip = True

            elif mode == FilterMode.Regex:
                regex = Filters.create_regex_filter(_filter, self.__log)

                if not Filters.filter_regex(value, regex):
                    skip = True

            elif mode == FilterMode.Like:
                if not Filters.filter_like(value, _filter):
                    skip = True

            if skip:
                self.__log.debug(f"Filter device ({device}). Filtered by '{mode.name}'")
                continue

            self.__log.debug(f"Append device ({device}).")
            filtered.append(device)

        return filtered

    def __usb_ipd_attach(self, device: Device) -> bool:
        self.__log.debug(f'Try attach usbipd device ({device}).')
        code, out = run([*self.CMD_ATTACH, device.bus_id()])

        if code > 0:
            self.__log.error(f"Error attaching device ({device}).\n{out}")
            return False

        self.__log.success(f'Success attach device ({device}).')

        return True

    def __usb_ipd_bind(self, device: Device, force: bool = False) -> bool:
        self.__log.debug(f'Try bind usbipd device ({device}).')
        cmd = self.CMD_BIND.copy()
        cmd.append(device.bus_id())

        if force:
            cmd.append(self._FORCE)

        code, out = run(cmd)

        if code > 0:
            self.__log.error(f'Bind failed device ({device}).\n{out}')
            return False

        self.__log.success(f'Success bind device ({device}).')

        return True

    def __usb_ipd_list(self) -> Tuple[bool, List[Device]]:
        self.__log.debug("Try getting usbipd devices")
        code, out = run(self.CMD_LIST)

        if code > 0:
            self.__log.error(f"Cannot get usbipd list.\n{out}")
            return False, []

        lines = out.split(os.linesep)

        devices = []

        for line in lines[2:]:
            if not line:
                break

            params = self.EMPTY.split(line)
            vid, pid = params[1].split(':')
            devices.append(Device(params[0], vid, pid, params[2], DeviceStatus(params[3])))

        return True, devices

    def __get_filtered_devices(self) -> List[Device]:
        ok, devices = self.__usb_ipd_list()

        if not ok:
            self.__log.error("Failed to get devices. Hypervisor stopped.")
            exit(1)

        if not len(devices):
            return []

        filtered: List[Device] = []

        for _filter in self.__devices_filters:
            filtered += self.__usb_ipd_filter(
                list(set(devices) - set(filtered)),
                _filter.filter_by(),
                _filter.value(),
                _filter.mode(),
            )

        return filtered

    def __run(self):
        while True:
            for device in self.__get_filtered_devices():
                if device.state() == DeviceStatus.Attached:
                    continue

                if device.state() == DeviceStatus.NotShared:
                    self.__usb_ipd_bind(device)
                    break

                if device.state() == DeviceStatus.Shared:
                    self.__usb_ipd_attach(device)
                    break

            if self.__timeout > 0:
                sleep(float(self.__timeout))
