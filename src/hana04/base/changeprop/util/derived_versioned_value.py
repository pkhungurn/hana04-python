from typing import List, Callable, TypeVar

from hana04.base.changeprop.abstract_derived_subject import AbstractDerivedSubject
from hana04.base.changeprop.versioned_subject import VersionedSubject
from hana04.base.changeprop.versioned_value import VersionedValue

T = TypeVar('T')


class DerivedVersionedValue(AbstractDerivedSubject, VersionedValue[T]):
    def __init__(self,
                 dependencies: List[VersionedValue],
                 new_version_func: Callable[[VersionedSubject, List[VersionedSubject]], int],
                 value_func: Callable[[], T]):
        super().__init__()
        self.dependencies = dependencies
        self.new_version_func = new_version_func
        self.value_func = value_func
        self.value = None

        for subject in self.dependencies:
            subject.add_observer(self)

        self._force_update()

    def update_internal(self) -> int:
        for subject in self.dependencies:
            subject.update()
        new_version = self.new_version_func(self, self.dependencies)
        self.value = self.value_func()
        return new_version

    def value(self) -> T:
        return self.value

