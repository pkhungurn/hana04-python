from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class FluentBuilder(Generic[T], ABC):
    @abstractmethod
    def build(self) -> T:
        pass


class FluentBuilderFactory(ABC):
    @abstractmethod
    def create(self) -> FluentBuilder:
        pass
