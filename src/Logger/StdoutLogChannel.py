from typing import Optional

from src.Ini import Ini
from src.Logger.AbstractLogChannel import AbstractLogChannel
from src.Logger.LogHelper import LogHelper
from src.Utils.Wrapper import Wrapper


class StdoutLogChannel(AbstractLogChannel):
    ERROR_TEXT_COLOR = "#FFFFFF"

    COLORS = {
        "info": "#3F74BA",
        "error": "#D64D5B",
        "warning": "#E4B40F",
        "success": "#5B9561",
        "debug": "#415294",
    }

    def __init__(self, ini: Ini):
        self.__wrapper = Wrapper()

        self.__level = ini.get('logger.stdout.level')
        self.__colorize = ini.get('logger.stdout.colorize', bool)
        self.__importance = LogHelper.get_importance(self.__level)

    def append(self, message: str, log_level: str, subject: Optional[dict] = None):
        if LogHelper.get_importance(log_level) < self.__importance:
            return

        message = LogHelper.get_log(log_level, message, subject)

        if self.__colorize:
            if log_level == LogHelper.LOG_LEVEL_ERROR:
                message = self.__wrap_error_message(message)
            else:
                message = self.__wrap_message(message, log_level)

        print(message)

    def __wrap_error_message(self, message: str) -> str:
        bg_color = self.COLORS['error']

        return self.__wrapper.background_color(self.__wrapper.color(message, self.ERROR_TEXT_COLOR), bg_color)

    def __wrap_message(self, message: str, log_level: str) -> str:
        return self.__wrapper.color(message, self.COLORS[log_level])
