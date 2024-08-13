class Math:
    @staticmethod
    def clamp(_num: int, _min: int, _max: int) -> int:
        return max(min(_num, _max), _min)

    @staticmethod
    def int2hex(data: int) -> str:
        return f"{data:0x}"

    @staticmethod
    def hex2int(data: str) -> int:
        return int(data[:2], 16)
