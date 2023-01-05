from typing import Dict, Any

from hana04.base.extension.extensions.do_nothing_extension import DoNothingExtension
from hana04.base.extension.hana_extensible import HanaExtensible
from hana04.base.extension.hana_extension_factory import HanaExtensionFactory, HanaExtensionFactoryMap
from hana04.base.extension.hana_extension_uber_factory import HanaExtensionUberFactory
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import injectable_class, memoized


class HanaExtensible_HanaExtensionFactory(HanaExtensionFactory[HanaExtensible]):
    pass


@memoized
@injectable_class
class HanaExtensible_DoNothingExtensionFactory(HanaExtensible_HanaExtensionFactory):
    def create(self, extensible: HanaExtensible) -> Any:
        return DoNothingExtension()


@memoized
@injectable_class
class HanaExtensible_ExtensionFactoryMap(HanaExtensionFactoryMap):
    def __init__(self, type_to_extension_factory: Dict[type, HanaExtensible_HanaExtensionFactory]):
        self.type_to_extension_factory = type_to_extension_factory

    @property
    def value(self) -> Dict[type, HanaExtensionFactory]:
        return self.type_to_extension_factory

    class Module(JyuusuModule):
        def configure(self, binder: Binder):
            binder.install_dict(type, HanaExtensible_HanaExtensionFactory)
            binder.install_class(HanaExtensible_ExtensionFactoryMap)
            binder.install_module(HanaExtensionUberFactory.Module)
            binder.bind_to_dict(type, HanaExtensionFactoryMap) \
                .with_key(HanaExtensible) \
                .to_type(HanaExtensible_ExtensionFactoryMap)


class HanaExtensible_Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(HanaExtensible_ExtensionFactoryMap.Module)
        binder.install_class(HanaExtensible_DoNothingExtensionFactory)
        binder.bind_to_dict(type, HanaExtensible_HanaExtensionFactory) \
            .with_key(DoNothingExtension) \
            .to_type(HanaExtensible_DoNothingExtensionFactory)
