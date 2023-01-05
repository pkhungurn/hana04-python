from abc import ABC, abstractmethod
from dataclasses import dataclass
from threading import Lock
from typing import Generic, TypeVar, Dict, Any

from hana04.base.caching.cache_key import CacheKey
from hana04.base.caching.hana_cache_loader import HanaCacheLoader, HanaCacheLoaderModule
from jyuusu.binder import Binder
from jyuusu.constructor_resolver import injectable_class
from jyuusu.provider import Lazy

T = TypeVar('T')


class Wrapped(Generic[T], ABC):
    @abstractmethod
    def unwrap(self, unwrapper: 'HanaUnwrapper') -> T:
        pass


@dataclass(eq=True, frozen=True)
class Cached(Wrapped[T]):
    key: CacheKey

    def unwrap(self, unwrapper: 'HanaUnwrapper') -> T:
        return unwrapper.unwrap(self)

    @staticmethod
    def of(key: CacheKey):
        return Cached(key)


class Direct(Wrapped[T]):
    def __init__(self, value: T):
        self.value = value

    def unwrap(self, unwrapper: 'HanaUnwrapper') -> T:
        return self.value

    @staticmethod
    def of(value: T):
        return Direct(value)


@injectable_class
class HanaUnwrapper:
    def __init__(self, protocol_to_cache_loader: Lazy[Dict[str, HanaCacheLoader]]):
        self.protocol_to_cache_loader = protocol_to_cache_loader
        self.string_key_to_obj: Dict[str, Any] = {}
        self.lock = Lock()

    def is_loaded(self, key: CacheKey):
        return key.string_key in self.string_key_to_obj

    def get(self, key: CacheKey):
        if not self.is_loaded(key):
            with self.lock:
                if key.string_key not in self.string_key_to_obj:
                    protocol_to_cache_loader = self.protocol_to_cache_loader.get()
                    assert key.protocol in protocol_to_cache_loader
                    loader = self.protocol_to_cache_loader.get()[key.protocol]
                    value = loader.load(key)
                    self.string_key_to_obj[key.string_key] = value
        return self.string_key_to_obj[key.string_key]

    def unwrap(self, wrapped: Wrapped[T]) -> T:
        if isinstance(wrapped, Direct):
            return wrapped.value
        elif isinstance(wrapped, Cached):
            return self.get(wrapped.key)
        else:
            raise AssertionError(f"'wrapped' is not one of the supported types! ({wrapped.__class__})")


def wrap_if_needed(value) -> Wrapped:
    if isinstance(value, Wrapped):
        return value
    else:
        return Direct.of(value)


class HanaUnwrapperModule:
    def configure(self, binder: Binder):
        binder.install_module(HanaCacheLoaderModule)
        binder.install_class(HanaUnwrapper)
