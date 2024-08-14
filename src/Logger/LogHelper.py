import os
from typing import Optional

from datetime import datetime


class LogHelper:
    LOG_LEVEL_DEBUG = 'debug'
    LOG_LEVEL_INFO = 'info'
    LOG_LEVEL_SUCCESS = 'success'
    LOG_LEVEL_WARNING = 'warning'
    LOG_LEVEL_ERROR = 'error'

    LOG_LEVELS_IMPORTANCE = {
        LOG_LEVEL_DEBUG: 1,
        LOG_LEVEL_INFO: 2,
        LOG_LEVEL_SUCCESS: 3,
        LOG_LEVEL_WARNING: 4,
        LOG_LEVEL_ERROR: 5,
    }

    @staticmethod
    def get_log_time() -> str:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_log_level(log_level: str) -> str:
        return log_level.upper()

    @staticmethod
    def get_log_prefix(_time: str, level: str) -> str:
        return f"[{_time}][{level}]"

    @staticmethod
    def subject_item_object(obj: object) -> str:
        if isinstance(obj, type):
            name = obj.__name__
        else:
            name = obj.__class__.__name__

        return f"{obj.__module__}.{name}"

    @staticmethod
    def subject_item_title(title: str) -> str:
        return title[0].upper() + title[1:].lower()

    @staticmethod
    def get_normal_log(message: str, subject: Optional[dict] = None) -> str:
        if subject:
            segments = []

            for key, val in subject.items():
                val = getattr(LogHelper, f'subject_item_{key}')(val)

                segments.append(f"{key}: {val}")

            subject = '|'.join(segments)

        prefix = f"[{subject}]: " if subject else ""

        return f"{prefix}{message}"

    @staticmethod
    def get_verbose_log(_time: str, level: str, message: str, subject: Optional[dict] = None):
        prefix = LogHelper.get_log_prefix(_time, level)
        message = LogHelper.get_normal_log(message, subject)

        return f"{prefix}{'' if subject else ': '}{message}"

    @staticmethod
    def get_log(log_level: str, message: str, subject: Optional[dict] = None):
        _time = LogHelper.get_log_time()
        level = LogHelper.get_log_level(log_level)

        return LogHelper.get_verbose_log(_time, level, message, subject)

    @staticmethod
    def get_importance(level: str) -> bool:
        return LogHelper.LOG_LEVELS_IMPORTANCE[level]

    @staticmethod
    def create_dir_log_if_not_exists(path: str):
        if not os.path.exists(_dir := os.path.dirname(path)):
            os.makedirs(_dir, exist_ok=True)
