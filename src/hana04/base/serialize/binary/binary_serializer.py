from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic, Dict, Any
from uuid import UUID, uuid4

from hana04.base.extension.hana_extensible import HanaExtensible
from hana04.base.serialize.binary.constants import TYPE_TAG, VALUE_TAG, UUID_TAG
from hana04.base.type_ids import TYPE_ID_LOOKUP
from hana04.base.util.message_packer import MessagePacker
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import injectable_class, memoized

T = TypeVar("T")


class TypeBinarySerializer(Generic[T], ABC):
    @abstractmethod
    def serialize(self, obj: T, packer: MessagePacker, serializer: 'BinarySerializer'):
        pass

    @abstractmethod
    def get_type_id(self) -> int:
        pass


@memoized
@injectable_class
class TypeIdToBinarySerializerMap:
    def __init__(self, value: Dict[int, TypeBinarySerializer]):
        self.value = value


@memoized
@injectable_class
class TypeToBinarySerializerMap:
    def __init__(self, value: Dict[type, TypeBinarySerializer]):
        self.value = value


class BinarySerializer:
    def __init__(self,
                 packer: MessagePacker,
                 file_name: Optional[str],
                 type_id_to_serializer: Dict[int, TypeBinarySerializer],
                 type_to_serializer: Dict[type, TypeBinarySerializer]):
        self.type_to_serializer = type_to_serializer
        self.type_id_to_serializer = type_id_to_serializer
        self.file_name = file_name
        self.packer = packer
        self.obj_id_to_uuid: Dict[int, UUID] = {}

    def serialize(self, obj: Any):
        from hana04.base.serialize.hana_serializable import HanaSerializable

        if isinstance(obj, HanaSerializable):
            if id(obj) in self.obj_id_to_uuid:
                self.pack_lookup(obj)
            else:
                serializer = self.type_id_to_serializer[obj.get_serialized_type_id()]
                self.pack_serializable(obj, serializer)
        else:
            serializer = self.type_to_serializer[obj.__class__]
            self.pack_non_serializable(obj, serializer)

    def pack_lookup(self, obj: Any):
        assert id(obj) in self.obj_id_to_uuid
        uuid = self.obj_id_to_uuid[id(obj)]
        self.packer.pack_map_header(2)
        if True:
            self.packer.pack_int(TYPE_TAG)
            self.packer.pack_int(TYPE_ID_LOOKUP)
        if True:
            self.packer.pack_int(VALUE_TAG)
            self.packer.pack_bytes(uuid.bytes)

    def pack_serializable(self, obj, serializer: TypeBinarySerializer):
        self.packer.pack_map_header(3)
        if True:
            self.packer.pack_int(TYPE_TAG)
            self.packer.pack_int(obj.get_serialized_type_id())
        if True:
            self.packer.pack_int(VALUE_TAG)
            serializer.serialize(obj, self.packer, self)
        if True:
            uuid = uuid4()
            self.obj_id_to_uuid[id(obj)] = uuid
            self.packer.pack_int(UUID_TAG)
            self.packer.pack_bytes(uuid.bytes)

    def pack_non_serializable(self, obj, serializer: TypeBinarySerializer):
        self.packer.pack_map_header(2)
        if True:
            self.packer.pack_int(TYPE_TAG)
            self.packer.pack_int(serializer.get_type_id())
        if True:
            self.packer.pack_int(VALUE_TAG)
            serializer.serialize(obj, self.packer, self)

    def serialize_extensions(self, hana_extensible: HanaExtensible):
        from hana04.base.serialize.hana_late_deserializable import HanaLateDeserializable

        serialized_extensions = [
            extension for extension in hana_extensible.get_extensions() if
            isinstance(extension, HanaLateDeserializable)]
        self.packer.pack_array_header(len(serialized_extensions))
        for extension in serialized_extensions:
            self.serialize(extension)

    @injectable_class
    class Factory:
        def __init__(self,
                     type_id_to_serializer: TypeIdToBinarySerializerMap,
                     type_to_serializer: TypeToBinarySerializerMap):
            self.type_to_serializer = type_to_serializer.value
            self.type_id_to_serializer = type_id_to_serializer.value

        def create(self, packer: MessagePacker, file_name: Optional[str] = None):
            return BinarySerializer(packer, file_name, self.type_id_to_serializer, self.type_to_serializer)

    class Module(JyuusuModule):
        def configure(self, binder: Binder):
            binder.install_dict(int, TypeBinarySerializer)
            binder.install_class(TypeIdToBinarySerializerMap)
            binder.install_dict(type, TypeBinarySerializer)
            binder.install_class(TypeToBinarySerializerMap)
            binder.install_class(BinarySerializer.Factory)
