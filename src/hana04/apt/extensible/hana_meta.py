import inspect
import typing
from typing import Optional, Any

from hana04.apt.extensible.constants import HANA_META_PROPERTY_NAME
from hana04.base.extension.constants import HANA_EXTENSIBLE_SUPER_TYPE_TAG
from hana04.base.extension.extensions.do_nothing_extension import DoNothingExtension
from hana04.base.extension.hana_extension_factory import HanaExtensionFactory, HanaExtensionFactoryMap
from hana04.base.extension.hana_extension_uber_factory import HanaExtensionUberFactory
from hana04.base.extension.hana_object import HanaObject
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import memoized, injectable_class


class HanaMeta:
    def __init__(self):
        self._class_name: Optional[str] = None
        self._parent_class: Optional[type] = None
        self._extension_factory_class: Optional[type] = None
        self._extension_factory_map_class: Optional[type] = None
        self._interface_module: Optional[type] = None
        self._owning_class = None

    @property
    def class_name(self):
        return self._class_name

    @property
    def owning_class(self):
        return self._owning_class

    @property
    def parent_class(self):
        return self._parent_class

    @property
    def interface_module(self):
        return self._interface_module

    @property
    def extension_factory_class(self):
        return self._extension_factory_class

    @property
    def extension_factory_map_class(self):
        return self._extension_factory_map_class

    @property
    def module(self):
        return self.interface_module

    def install_module(self, binder: Binder):
        binder.install_module(self.module)

    @staticmethod
    def assert_hana_interface_can_be_created(cls: type):
        assert inspect.isclass(cls)
        assert HANA_META_PROPERTY_NAME in cls.__dict__
        assert isinstance(cls.__dict__[HANA_META_PROPERTY_NAME], HanaMeta)
        assert len(cls.__bases__) == 1
        assert issubclass(cls, HanaObject)

    @staticmethod
    def assert_is_hana_interface(cls: type):
        HanaMeta.assert_hana_interface_can_be_created(cls)
        hana_meta: HanaMeta = cls.__dict__[HANA_META_PROPERTY_NAME]
        assert hana_meta.owning_class == cls

    def make_hana_interface(self, cls):
        assert cls.__dict__[HANA_META_PROPERTY_NAME] == self
        self._class_name = cls.__name__
        self._parent_class = cls.__bases__[0]
        self._owning_class = cls
        this = self

        class _HanaExtensionFactory(HanaExtensionFactory[cls]):
            pass

        @memoized
        @injectable_class
        class _DoNothingExtensionFactory(_HanaExtensionFactory):
            def create(self, extensible: cls) -> Any:
                return DoNothingExtension()

        @memoized
        @injectable_class
        class _HanaExtensionFactoryMap(HanaExtensionFactoryMap):
            def __init__(self, type_to_extension_factory: typing.Dict[type, _HanaExtensionFactory]):
                self.type_to_extension_factory = type_to_extension_factory

            @property
            def value(self) -> typing.Dict[type, HanaExtensionFactory]:
                return self.type_to_extension_factory

            class Module(JyuusuModule):
                def configure(self, binder: Binder):
                    binder.install_dict(type, _HanaExtensionFactory)
                    binder.install_class(_HanaExtensionFactoryMap)
                    binder.install_module(HanaExtensionUberFactory.Module)
                    binder.bind_to_dict(type, HanaExtensionFactoryMap) \
                        .with_key(cls) \
                        .to_type(_HanaExtensionFactoryMap)

        class _HanaInterfaceModule(JyuusuModule):
            def configure(self, binder: Binder):
                binder.install_module(HanaExtensionUberFactory.Module)
                binder.bind_to_dict(type, type, HANA_EXTENSIBLE_SUPER_TYPE_TAG) \
                    .with_key(cls) \
                    .to_instance(this._parent_class)

                binder.install_module(_HanaExtensionFactoryMap.Module)
                binder.install_class(_DoNothingExtensionFactory)
                binder.bind_to_dict(type, _HanaExtensionFactory) \
                    .with_key(DoNothingExtension) \
                    .to_type(_DoNothingExtensionFactory)

        self._extension_factory_class = _HanaExtensionFactory
        self._extension_factory_map_class = _HanaExtensionFactoryMap
        self._interface_module = _HanaInterfaceModule


def hana_meta(cls) -> HanaMeta:
    assert inspect.isclass(cls)
    assert "_HANA_META" in cls.__dict__
    assert isinstance(cls._HANA_META, HanaMeta)
    return cls._HANA_META


def hana_module(cls):
    return hana_meta(cls).module