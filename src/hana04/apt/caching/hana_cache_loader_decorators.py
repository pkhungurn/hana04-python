import inspect

from hana04.base.caching.hana_cache_loader import HanaCacheLoader
from hana04.base.caching.wrapped import HanaUnwrapperModule
from jyuusu.binder import Binder
from jyuusu.constructor_resolver import is_class_injectable, injectable_class


def hana_cache_loader(protocol: str):
    def func(cls):
        assert inspect.isclass(cls)
        assert issubclass(cls, HanaCacheLoader)
        if not is_class_injectable(cls):
            injectable_class(cls)

        class _HanaCacheLoaderModule:
            def configure(self, binder: Binder):
                binder.install_class(cls)
                binder.install_module(HanaUnwrapperModule)
                binder.bind_to_dict(str, HanaCacheLoader).with_key(protocol).to_type(cls)

        cls._HanaCacheLoaderModule = _HanaCacheLoaderModule
        return cls

    return func


def hana_cache_loader_module(cls):
    assert "_HanaCacheLoaderModule" in cls.__dict__
    return cls._HanaCacheLoaderModule
