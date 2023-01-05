from typing import TypeVar

from hana04.base.changeprop.versioned_subject import DirtinessObserver
from hana04.base.changeprop.versioned_value import VersionedValue

T = TypeVar('T')


class Constant(VersionedValue[T]):
    def __init__(self, value: T):
        self._value = value

    def value(self) -> T:
        return self.value

    def add_observer(self, dirtiness_observer: DirtinessObserver):
        # NO-OP
        pass

    def remove_observe(self, dirtiness_observer: DirtinessObserver):
        # NO-OP
        pass

    def version(self) -> int:
        return 0

    def update(self):
        # NO-OP
        pass

    def is_dirty(self) -> bool:
        return False
