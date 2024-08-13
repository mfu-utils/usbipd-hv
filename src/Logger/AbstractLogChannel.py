from abc import ABC, abstractmethod
from typing import Optional


class AbstractLogChannel(ABC):
    @abstractmethod
    def append(self, message: str, log_level: str, subject: Optional[dict] = None) -> None:
        pass
