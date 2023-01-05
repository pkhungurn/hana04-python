from threading import Lock


class AtomicBoolean:
    def __init__(self):
        self._value = False
        self.lock = Lock()

    def get(self):
        with self.lock:
            return self._value

    def set(self, value: bool):
        with self.lock:
            self._value = value

    def get_and_set(self, new_value: bool):
        with self.lock:
            old_value = self._value
            self._value = new_value
            return old_value