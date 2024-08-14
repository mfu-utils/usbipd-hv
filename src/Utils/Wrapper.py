from typing import Union

from src.Utils.Color import Color

ESC = '\x1b'
END = '0m'

START = f"{ESC}["
STOP = f"{ESC}[{END}"

RGB_COLOR_START = f"{START}38;2;"
RGB_BG_COLOR_START = f"{START}48;2;"


class Wrapper:
    @staticmethod
    def get_rgb_as_text(color: Union[Color, str]) -> str:
        if not type(color) is Color:
            color = Color(color)

        return color.get_rgb_as_text(";")

    @staticmethod
    def color(message: str, color: Union[Color, str]) -> str:
        rgb = Wrapper.get_rgb_as_text(color)

        return f"{RGB_COLOR_START}{rgb}m{message}{STOP}"

    @staticmethod
    def background_color(message: str, color: Union[Color, str]) -> str:
        rgb = Wrapper.get_rgb_as_text(color)

        return f"{RGB_BG_COLOR_START}{rgb}m{message}{STOP}"
