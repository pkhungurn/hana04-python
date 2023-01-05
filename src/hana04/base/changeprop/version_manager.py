from threading import Lock


class VersionManager:
    def __init__(self):
        self.lock = Lock()
        self._version = 0

    def get_version(self):
        with self.lock:
            return self._version

    def bump_version(self):
        with self.lock:
            self._version += 1
            return self._version

    def set_version(self, new_version):
        with self.lock:
            assert new_version > self._version
            self._version = new_version
