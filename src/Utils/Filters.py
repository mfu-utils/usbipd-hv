import re
from typing import Optional

from src.Log import Log


class Filters:
    REGEX_CACHE = {}

    @staticmethod
    def filter_like(value: str, _filter: str) -> bool:
        if start := _filter[0] == "*":
            _filter = _filter[1:]

        if end := _filter[-1] == "*":
            _filter = _filter[:-1]

        segments = value.split(_filter)

        if len(segments) < 3:
            return False

        if not start and segments[0]:
            return False

        if not end and segments[-1]:
            return False

        return True

    @staticmethod
    def create_regex_filter(_filter: str, log: Log) -> Optional[re.Pattern]:
        try:
            if not (r := Filters.REGEX_CACHE.get(_filter)):
                r = re.compile(_filter)
                Filters.REGEX_CACHE[_filter] = r

            return r

        except re.error:
            log.error(f"Cannot create filter from regex: ({_filter}).")
            return None

    @staticmethod
    def filter_regex(value: str, _filter: re.Pattern) -> bool:
        return bool(_filter.match(value))

    @staticmethod
    def filter_key(value: str, _filter: str) -> bool:
        if _filter == "*":
            return True

        return value == _filter
