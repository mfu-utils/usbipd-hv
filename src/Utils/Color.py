import re

from typing import Union, Tuple, List

from src.Utils.Math import Math

COLOR_HEX_RE = re.compile(r'[0-9a-fA-F]{6}')


class Color:
    def __init__(self, data: Union[str, Tuple[int, int, int]]):
        self.color: List[int] = [0, 0, 0]

        if type(data) is tuple:
            for i, num in enumerate(data):
                self.color[i] = Math.clamp(int(num), 0, 255)

        if not data:
            raise Exception("Color is null")

        self.color = Color.hex2rgb(data)

    @staticmethod
    def hex2rgb(data: str) -> list:
        if len(data) != 7 or data[0] != '#' or not len(COLOR_HEX_RE.findall(data[1:])):
            raise Exception(f"Error parse color '{data}'")

        data = data[1:]

        r = data[:2]
        g = data[2:4]
        b = data[4:]

        return [Math.hex2int(r), Math.hex2int(g), Math.hex2int(b)]

    def get_rgb_as_text(self, delimiter: str = ","):
        return delimiter.join(list(map(lambda x: str(x), self.color)))
