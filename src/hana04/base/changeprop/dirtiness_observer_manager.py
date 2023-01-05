import weakref
from threading import Lock

from hana04.base.changeprop.versioned_subject import VersionedSubject, DirtinessObserver


class DirtinessObserverManager:
    def __init__(self, versioned_subject: VersionedSubject):
        self.versioned_subject = versioned_subject
        self.lock = Lock()
        self.observers: weakref.WeakSet[DirtinessObserver] = weakref.WeakSet()

    def add_observer(self, dirtiness_observer: DirtinessObserver):
        with self.lock:
            self.observers.add(dirtiness_observer)

    def remove_observer(self, dirtiness_observer: DirtinessObserver):
        with self.lock:
            self.observers.remove(dirtiness_observer)

    def notify_observers(self):
        with self.lock:
            for observer in self.observers:
                observer.notified_dirtiness(self)

