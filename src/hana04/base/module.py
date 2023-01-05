from hana04.base.caching.hana_cache_loader import HanaCacheLoaderModule
from hana04.base.caching.wrapped import HanaUnwrapperModule
from hana04.base.extension.hana_customized_builders import HanaCustomizedBuilderModule
from hana04.base.extension.hana_extensibles import HanaExtensible_Module
from hana04.base.extension.hana_extension_uber_factory import HanaExtensionUberFactory
from hana04.base.extension.hana_objects import HanaObject_Module
from hana04.base.serialize.binary.binary_deserializer import BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import BinarySerializer
from hana04.base.serialize.file_deserializer import FileDeserializer
from hana04.base.serialize.file_serializer import FileSerializer
from hana04.base.serialize.hana_late_deserializables import HanaLateDeserializable_Module
from hana04.base.serialize.readable.readable_deserializer import ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import ReadableSerializer
import hana04.base.util.hana_map_entry
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.injectors import create_injector


class HanaBaseModule(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(BinaryDeserializer.Module)
        binder.install_module(BinarySerializer.Module)
        binder.install_module(ReadableDeserializer.Module)
        binder.install_module(ReadableSerializer.Module)
        binder.install_module(HanaExtensionUberFactory.Module)
        binder.install_module(HanaExtensible_Module)
        binder.install_module(HanaObject_Module)
        binder.install_module(HanaLateDeserializable_Module)
        binder.install_module(hana04.base.util.hana_map_entry.Module)
        binder.install_module(HanaCustomizedBuilderModule)
        binder.install_module(HanaCacheLoaderModule)
        binder.install_module(HanaUnwrapperModule)

        binder.install_module(FileSerializer.Module)
        binder.install_module(FileDeserializer.Module)


if __name__ == "__main__":
    injector = create_injector(HanaBaseModule)
    extension_uber_factory: HanaExtensionUberFactory = injector.get_instance(HanaExtensionUberFactory)
    injector.get_instance(BinarySerializer.Factory)

    print(extension_uber_factory.super_type_map)
