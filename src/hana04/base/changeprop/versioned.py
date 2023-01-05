from abc import ABC, abstractmethod


class Versioned(ABC):
    @abstractmethod
    def version(self) -> int:
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def is_dirty(self) -> bool:
        pass
