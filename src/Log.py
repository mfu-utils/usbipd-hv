from typing import Optional

from src.Ini import Ini
from src.Logger.AbstractLogChannel import AbstractLogChannel
from src.Logger.LogHelper import LogHelper
from src.Logger.StackLogChannel import StackLogChannel
from src.Utils.Wrapper import Wrapper


class Log:
    def __init__(self, ini: Ini):
        self.__channel: AbstractLogChannel = StackLogChannel(ini)
        self.__wrapper = Wrapper()

        self.__enabled = ini.get('app.debug', bool)

    def log(self, log_level: str, message: str, subject: Optional[dict] = None):
        if not self.__enabled:
            return

        self.__channel.append(log_level, message, subject)

    def info(self, message: str, subject: Optional[dict] = None):
        self.log(message, LogHelper.LOG_LEVEL_INFO, subject)

    def error(self, message: str, subject: Optional[dict] = None):
        self.log(message, LogHelper.LOG_LEVEL_ERROR, subject)

    def warning(self, message: str, subject: Optional[dict] = None):
        self.log(message, LogHelper.LOG_LEVEL_WARNING, subject)

    def success(self, message: str, subject: Optional[dict] = None):
        self.log(message, LogHelper.LOG_LEVEL_SUCCESS, subject)

    def debug(self, message: str, subject: Optional[dict] = None):
        self.log(message, LogHelper.LOG_LEVEL_DEBUG, subject)

