from src.Hypervisor import Hypervisor
from src.Ini import Ini
from src.Log import Log

INI_FILE_PATH = "config.ini"


def main():
    ini = Ini(INI_FILE_PATH)
    log = Log(ini)
    Hypervisor(ini, log)


if __name__ == "__main__":
    main()
