from enum import Enum


class DeviceStatus(Enum):
    NotShared = 'Not shared'
    Shared = 'Shared'
    Attached = 'Attached'
