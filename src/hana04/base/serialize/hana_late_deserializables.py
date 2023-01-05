from typing import Any, Dict

from hana04.base.extension.constants import HANA_EXTENSIBLE_SUPER_TYPE_TAG
from hana04.base.extension.extensions.do_nothing_extension import DoNothingExtension
from hana04.base.extension.hana_extension_factory import HanaExtensionFactory, HanaExtensionFactoryMap
from hana04.base.extension.hana_extension_uber_factory import HanaExtensionUberFactory
from hana04.base.extension.hana_object import HanaObject
from hana04.base.serialize.hana_late_deserializable import HanaLateDeserializable
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import memoized, injectable_class


class HanaLateDeserializable_ExtensionFactory(HanaExtensionFactory[HanaLateDeserializable]):
    pass


@memoized
@injectable_class
class HanaLateDeserializable_DoNothingExtensionFactory(HanaLateDeserializable_ExtensionFactory):
    def create(self, extensible: HanaLateDeserializable) -> Any:
        return DoNothingExtension()


@memoized
@injectable_class
class HanaLateDeserializable_ExtensionFactoryMap(HanaExtensionFactoryMap):
    def __init__(self, type_to_extension_factory: Dict[type, HanaLateDeserializable_ExtensionFactory]):
        self.type_to_extension_factory = type_to_extension_factory

    @property
    def value(self) -> Dict[type, HanaExtensionFactory]:
        return self.type_to_extension_factory

    class Module(JyuusuModule):
        def configure(self, binder: Binder):
            binder.install_dict(type, HanaLateDeserializable_ExtensionFactory)
            binder.install_class(HanaLateDeserializable_ExtensionFactoryMap)
            binder.install_module(HanaExtensionUberFactory.Module)
            binder.bind_to_dict(type, HanaExtensionFactoryMap) \
                .with_key(HanaLateDeserializable) \
                .to_type(HanaLateDeserializable_ExtensionFactoryMap)


class HanaLateDeserializable_Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(HanaExtensionUberFactory.Module)
        binder.bind_to_dict(type, type, HANA_EXTENSIBLE_SUPER_TYPE_TAG) \
            .with_key(HanaLateDeserializable) \
            .to_instance(HanaObject)

        binder.install_module(HanaLateDeserializable_ExtensionFactoryMap.Module)
        binder.install_class(HanaLateDeserializable_DoNothingExtensionFactory)
        binder.bind_to_dict(type, HanaLateDeserializable_ExtensionFactory) \
            .with_key(DoNothingExtension) \
            .to_type(HanaLateDeserializable_DoNothingExtensionFactory)
