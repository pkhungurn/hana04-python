from abc import ABC, abstractmethod

from hana04.base.changeprop.versioned import Versioned


class DirtinessObserver(ABC):
    @abstractmethod
    def notified_dirtiness(self, versioned_subject: 'VersionedSubject'):
        pass


class VersionedSubject(Versioned, ABC):
    @abstractmethod
    def add_observer(self, dirtiness_observer: DirtinessObserver):
        pass

    @abstractmethod
    def remove_observe(self, dirtiness_observer: DirtinessObserver):
        pass