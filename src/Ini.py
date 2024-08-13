import configparser
from typing import Optional, Any

from src.Utils.Cast import Casts


class Ini:
    def __init__(self, path: str) -> None:
        self.path = path

        self.data = None

        self.load()

    def load(self):
        self.data = configparser.ConfigParser()
        self.data.read(self.path)

    def get(self, dot_path: str, _type: Optional[type] = None) -> Any:
        try:
            segments = dot_path.split('.')

            data = self.data.get('.'.join(segments[:-1]), segments[-1])

            if _type is not None:
                return Casts.str_to(data, _type)

            return data
        except ValueError:
            return None

    def set(self, dot_path: str, value):
        section, option = dot_path.split('.')

        self.data.set(section, option, str(value))

    def write(self):
        with open(self.path, 'w') as configfile:
            self.data.write(configfile)

        self.load()
