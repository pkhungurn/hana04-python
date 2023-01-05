from abc import ABC

from hana04.base.changeprop.abstract_versioned_subject import AbstractVersionedSubject
from hana04.base.changeprop.versioned_subject import DirtinessObserver, VersionedSubject


class AbstractDerivedSubject(AbstractVersionedSubject, DirtinessObserver, ABC):
    def __init__(self):
        super().__init__()

    def notified_dirtiness(self, versioned_subject: VersionedSubject):
        was_dirty = self._dirty_bit.get_and_set(True)
        if not was_dirty:
            self._dirtiness_observer_manager.notify_observers()
