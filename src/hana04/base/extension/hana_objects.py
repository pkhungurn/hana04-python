from typing import Any, Dict

from hana04.base.extension.constants import HANA_EXTENSIBLE_SUPER_TYPE_TAG
from hana04.base.extension.extensions.do_nothing_extension import DoNothingExtension
from hana04.base.extension.hana_extensible import HanaExtensible
from hana04.base.extension.hana_extension_factory import HanaExtensionFactory, HanaExtensionFactoryMap
from hana04.base.extension.hana_extension_uber_factory import HanaExtensionUberFactory
from hana04.base.extension.hana_object import HanaObject
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import injectable_class, memoized


class HanaObject_HanaExtensionFactory(HanaExtensionFactory[HanaObject]):
    pass


@memoized
@injectable_class
class HanaObject_DoNothingExtensionFactory(HanaObject_HanaExtensionFactory):
    def create(self, extensible: HanaObject) -> Any:
        return DoNothingExtension()


@memoized
@injectable_class
class HanaObject_ExtensionFactoryMap(HanaExtensionFactoryMap):
    def __init__(self, type_to_extension_factory: Dict[type, HanaObject_HanaExtensionFactory]):
        self.type_to_extension_factory = type_to_extension_factory

    @property
    def value(self) -> Dict[type, HanaExtensionFactory]:
        return self.type_to_extension_factory

    class Module(JyuusuModule):
        def configure(self, binder: Binder):
            binder.install_dict(type, HanaObject_HanaExtensionFactory)
            binder.install_class(HanaObject_ExtensionFactoryMap)
            binder.install_module(HanaExtensionUberFactory.Module)
            binder.bind_to_dict(type, HanaExtensionFactoryMap) \
                .with_key(HanaObject) \
                .to_type(HanaObject_ExtensionFactoryMap)


class HanaObject_Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(HanaExtensionUberFactory.Module)
        binder.bind_to_dict(type, type, HANA_EXTENSIBLE_SUPER_TYPE_TAG) \
            .with_key(HanaObject) \
            .to_instance(HanaExtensible)

        binder.install_module(HanaObject_ExtensionFactoryMap.Module)
        binder.install_class(HanaObject_DoNothingExtensionFactory)
        binder.bind_to_dict(type, HanaObject_HanaExtensionFactory) \
            .with_key(DoNothingExtension) \
            .to_type(HanaObject_DoNothingExtensionFactory)
