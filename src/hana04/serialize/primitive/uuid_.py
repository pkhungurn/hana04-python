from typing import Dict, Any
from uuid import UUID

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_binary_deserializer_module, \
    hana_binary_serializer_module, hana_readable_deserializer_module, hana_readable_serializer_module
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.serialize.type_ids import TYPE_ID_UUID, TYPE_NAME_UUID
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import injectable_class, memoized


@hana_readable_serializer_by_type(UUID)
@memoized
@injectable_class
class UuidReadableSerializer(TypeReadableSerializer[UUID]):
    def serialize(self, obj: UUID, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_UUID,
            "value": str(obj)
        }


@hana_readable_deserializer(TYPE_NAME_UUID)
@memoized
@injectable_class
class UuidReadableDeserializer(TypeReadableDeserializer[UUID]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> UUID:
        return UUID(json["value"])

    def get_serialized_type(self) -> type:
        return UUID


@hana_binary_serializer_by_type(UUID)
@memoized
@injectable_class
class UuidBinarySerializer(TypeBinarySerializer[UUID]):
    def serialize(self, obj: UUID, packer: MessagePacker, serializer: BinarySerializer):
        packer.pack_bytes(obj.bytes)

    def get_type_id(self) -> int:
        return TYPE_ID_UUID


@hana_binary_deserializer(TYPE_ID_UUID)
@memoized
@injectable_class
class UuidBinaryDeserializer(TypeBinaryDeserializer[UUID]):
    def deserialize(self, value: Any, binary_deserializer: BinaryDeserializer) -> UUID:
        return UUID(bytes=value)

    def get_serialized_type(self) -> type:
        return UUID


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(UuidReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(UuidReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(UuidBinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(UuidBinarySerializer))
