import os

from src.Hypervisor import Hypervisor
from src.Ini import Ini
from src.Log import Log

from config import INI_FILE_PATH


def main():
    os.system('COLOR 0')
    ini = Ini(INI_FILE_PATH)
    log = Log(ini)
    Hypervisor(ini, log)


if __name__ == "__main__":
    main()
