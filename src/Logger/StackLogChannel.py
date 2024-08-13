from typing import List, Optional

from src.Ini import Ini
from src.Logger.AbstractLogChannel import AbstractLogChannel
from src.Logger.FileLogChannel import FileLogChannel
from src.Logger.StdoutLogChannel import StdoutLogChannel


class StackLogChannel(AbstractLogChannel):
    def __init__(self, ini: Ini):
        self.__channels: List[AbstractLogChannel] = [FileLogChannel(ini)]

        if ini.get('app.debug', bool):
            self.__channels.append(StdoutLogChannel(ini))

    def append(self, message: str, log_level: str, subject: Optional[dict] = None):
        for channel in self.__channels:
            channel.append(message, log_level, subject)
