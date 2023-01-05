from abc import ABC, abstractmethod

from hana04.base.util.atomic_boolean import AtomicBoolean
from hana04.base.changeprop.dirtiness_observer_manager import DirtinessObserverManager
from hana04.base.changeprop.version_manager import VersionManager
from hana04.base.changeprop.versioned_subject import VersionedSubject, DirtinessObserver


class AbstractVersionedSubject(VersionedSubject, ABC):
    def __init__(self):
        self._version_manager = VersionManager()
        self._dirtiness_observer_manager = DirtinessObserverManager(self)
        self._dirty_bit = AtomicBoolean()

    @abstractmethod
    def update_internal(self) -> int:
        pass

    def is_dirty(self) -> bool:
        return self._dirty_bit.get()

    def update(self):
        if not self.is_dirty():
            return
        new_version = self.update_internal()
        self._dirty_bit.set(False)
        self._version_manager.set_version(new_version)

    def _force_update(self):
        self._dirty_bit.set(True)
        self.update()

    def version(self) -> int:
        return self._version_manager.get_version()

    def _mark_dirty(self):
        if self.is_dirty():
            return
        self._dirty_bit.set(True)
        self._dirtiness_observer_manager.notify_observers()

    def add_observer(self, dirtiness_observer: DirtinessObserver):
        self._dirtiness_observer_manager.add_observer(dirtiness_observer)

    def remove_observe(self, dirtiness_observer: DirtinessObserver):
        self._dirtiness_observer_manager.remove_observer(dirtiness_observer)
