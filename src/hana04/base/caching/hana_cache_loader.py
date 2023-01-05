from abc import ABC, abstractmethod

from hana04.base.caching.cache_key import CacheKey
from jyuusu.binder import Binder, Module as JyuusuModule


class HanaCacheLoader(ABC):
    @abstractmethod
    def load(self, key: CacheKey):
        pass


class HanaCacheLoaderModule(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_dict(str, HanaCacheLoader)
