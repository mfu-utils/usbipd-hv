from typing import Optional

from src.Ini import Ini
from src.Logger.AbstractLogChannel import AbstractLogChannel
from src.Logger.LogHelper import LogHelper


class FileLogChannel(AbstractLogChannel):
    def __init__(self, ini: Ini):

        self.__path = ini.get('logger.file.path')
        self.__level = ini.get('logger.file.level')
        self.__importance = LogHelper.get_importance(self.__level)

        LogHelper.create_dir_log_if_not_exists(self.__path)

    def append(self, message: str, log_level: str, subject: Optional[dict] = None):
        if LogHelper.get_importance(log_level) < self.__importance:
            return

        with open(self.__path, mode='a', encoding='utf-8') as f:
            f.write(f"{LogHelper.get_log(log_level, message, subject)}\n")
