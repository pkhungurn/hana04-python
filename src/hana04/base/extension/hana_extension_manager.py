from threading import Lock
from typing import Any, Dict, Iterable

from hana04.base.extension.hana_extensible import HanaExtensible
from hana04.base.extension.hana_extension_uber_factory import HanaExtensionUberFactory


class HanaExtensionManager:
    def __init__(self, extensible_type: type, extension_uber_factory: HanaExtensionUberFactory):
        self.__extensible_type = extensible_type
        self.__extension_uber_factory = extension_uber_factory
        self.__extensions: Dict[type, Any] = {}
        self.__lock = Lock()

    def supports_extension(self, klass: type) -> bool:
        return self.__extension_uber_factory.supports_extension(self.__extensible_type, klass)

    def get_extension(self, instance: HanaExtensible, klass: type):
        self.prepare_extension(instance, klass)
        return self.__extensions[klass]

    def create_extension(self, instance: HanaExtensible, klass: type):
        return self.__extension_uber_factory.create_extension(instance, self.__extensible_type, klass)

    def prepare_extension(self, instance: HanaExtensible, klass: type):
        if self.has_extension(klass):
            return
        with self.__lock:
            if not self.has_extension(klass):
                extension = self.create_extension(instance, klass)
                self.__extensions[klass] = extension

    def get_extensions(self) -> Iterable[Any]:
        return self.__extensions.values()

    def has_extension(self, klass: type) -> bool:
        return klass in self.__extensions
