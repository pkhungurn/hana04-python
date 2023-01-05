from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from hana04.base.changeprop.versioned_subject import VersionedSubject

T = TypeVar('T')


class VersionedValue(VersionedSubject, Generic[T], ABC):
    @abstractmethod
    def value(self) -> T:
        pass

    def updated_value(self):
        self.update()
        return self.value()