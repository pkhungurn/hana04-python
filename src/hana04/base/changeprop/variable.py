from contextlib import contextmanager
from typing import TypeVar

from hana04.base.changeprop.dirtiness_observer_manager import DirtinessObserverManager
from hana04.base.changeprop.version_manager import VersionManager
from hana04.base.changeprop.versioned_subject import DirtinessObserver
from hana04.base.changeprop.versioned_value import VersionedValue

T = TypeVar('T')


class Variable(VersionedValue[T]):
    def __init__(self, value: T):
        self._value = value
        self.observer_manager = DirtinessObserverManager(self)
        self.version_manager = VersionManager()

    def value(self) -> T:
        return self._value

    def add_observer(self, dirtiness_observer: DirtinessObserver):
        self.observer_manager.add_observer(dirtiness_observer)

    def remove_observe(self, dirtiness_observer: DirtinessObserver):
        self.observer_manager.remove_observer(dirtiness_observer)

    def version(self) -> int:
        return self.version_manager.get_version()

    def update(self):
        pass

    def is_dirty(self) -> bool:
        return False

    def set(self, new_value: T):
        self._value = new_value
        self.version_manager.bump_version()
        self.observer_manager.notify_observers()

    @contextmanager
    def mutate(self):
        yield self._value
        self.version_manager.bump_version()
        self.observer_manager.notify_observers()
