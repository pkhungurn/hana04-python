from typing import Dict, Any

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_binary_deserializer_module, \
    hana_binary_serializer_module, hana_readable_deserializer_module, hana_readable_serializer_module
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.serialize.type_ids import TYPE_ID_BOOLEAN, TYPE_NAME_BOOLEAN
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import injectable_class, memoized


@hana_readable_serializer_by_type(bool)
@memoized
@injectable_class
class BooleanReadableSerializer(TypeReadableSerializer[bool]):
    def serialize(self, obj: bool, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_BOOLEAN,
            "value": obj
        }


@hana_readable_deserializer(TYPE_NAME_BOOLEAN)
@memoized
@injectable_class
class BooleanReadableDeserializer(TypeReadableDeserializer[bool]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> bool:
        return bool(json["value"])

    def get_serialized_type(self) -> type:
        return bool


@hana_binary_serializer_by_type(bool)
@memoized
@injectable_class
class BooleanBinarySerializer(TypeBinarySerializer[bool]):
    def serialize(self, obj: bool, packer: MessagePacker, serializer: BinarySerializer):
        packer.pack_bool(obj)

    def get_type_id(self) -> int:
        return TYPE_ID_BOOLEAN


@hana_binary_deserializer(TYPE_ID_BOOLEAN)
@memoized
@injectable_class
class BooleanBinaryDeserializer(TypeBinaryDeserializer[bool]):
    def deserialize(self, value: Any, binary_deserializer: BinaryDeserializer) -> bool:
        assert isinstance(value, bool)
        return bool(value)

    def get_serialized_type(self) -> type:
        return bool


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(BooleanReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(BooleanReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(BooleanBinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(BooleanBinarySerializer))
