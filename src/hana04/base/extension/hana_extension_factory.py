from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any, Dict

from hana04.base.extension.hana_extensible import HanaExtensible

T = TypeVar('T', bound=HanaExtensible, covariant=True)


class HanaExtensionFactory(Generic[T], ABC):
    @abstractmethod
    def create(self, extensible: T) -> Any:
        pass


class HanaExtensionFactoryMap(ABC):
    @property
    @abstractmethod
    def value(self) -> Dict[type, HanaExtensionFactory]:
        pass
