from abc import ABC, abstractmethod
from typing import Any, Iterable


class HanaExtensible(ABC):
    @abstractmethod
    def has_extension(self, klass: type) -> bool:
        pass

    @abstractmethod
    def supports_extension(self, klass: type) -> bool:
        pass

    @abstractmethod
    def get_extension(self, klass: type):
        pass

    @abstractmethod
    def prepare_extension(self, klass: type):
        pass

    @abstractmethod
    def get_extensions(self) -> Iterable[Any]:
        pass
