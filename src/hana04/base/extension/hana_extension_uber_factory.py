from typing import Dict, Any

from hana04.base.extension.constants import HANA_EXTENSIBLE_SUPER_TYPE_TAG
from hana04.base.extension.hana_extensible import HanaExtensible
from hana04.base.extension.hana_extension_factory import HanaExtensionFactoryMap
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import memoized, injectable_class_with_specs


@memoized
@injectable_class_with_specs(super_type_map=HANA_EXTENSIBLE_SUPER_TYPE_TAG)
class HanaExtensionUberFactory:
    def __init__(self,
                 super_type_map: Dict[type, type],
                 type_to_extension_factory_map: Dict[type, HanaExtensionFactoryMap]):
        self.type_to_extension_factory_map = type_to_extension_factory_map
        self.super_type_map = super_type_map

    def supports_extension(self, extensible_type: type, extension_type: type) -> bool:
        current_extensible = extensible_type
        while True:
            extensible_factory_map = self.type_to_extension_factory_map[current_extensible]
            if extension_type in extensible_factory_map.value:
                return True
            if current_extensible not in self.super_type_map:
                break
            current_extensible = self.super_type_map[current_extensible]
        return False

    def create_extension(self, extensible: HanaExtensible, extensible_type: type, extension_type: type) -> Any:
        current_extensible = extensible_type
        while True:
            extensible_factory_map = self.type_to_extension_factory_map[current_extensible]
            if extension_type in extensible_factory_map.value:
                return extensible_factory_map.value[extension_type].create(extensible)
            if current_extensible not in self.super_type_map:
                break
            current_extensible = self.super_type_map[current_extensible]
        raise RuntimeError(f"Extension {extension_type} for type {extensible_type} is not supported")

    class Module(JyuusuModule):
        def configure(self, binder: Binder):
            binder.install_dict(type, type, HANA_EXTENSIBLE_SUPER_TYPE_TAG)
            binder.install_dict(type, HanaExtensionFactoryMap)
            binder.install_class(HanaExtensionUberFactory)
