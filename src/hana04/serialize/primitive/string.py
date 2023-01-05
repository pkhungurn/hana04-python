from typing import Dict, Any

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_binary_deserializer_module, \
    hana_binary_serializer_module, hana_readable_deserializer_module, hana_readable_serializer_module
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.serialize.type_ids import TYPE_ID_STRING, TYPE_NAME_STRING
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import injectable_class, memoized


@hana_readable_serializer_by_type(str)
@memoized
@injectable_class
class StringReadableSerializer(TypeReadableSerializer[str]):
    def serialize(self, obj: str, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_STRING,
            "value": obj
        }


@hana_readable_deserializer(TYPE_NAME_STRING)
@memoized
@injectable_class
class StringReadableDeserializer(TypeReadableDeserializer[str]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> str:
        return str(json["value"])

    def get_serialized_type(self) -> type:
        return str


@hana_binary_serializer_by_type(str)
@memoized
@injectable_class
class StringBinarySerializer(TypeBinarySerializer[str]):
    def serialize(self, obj: str, packer: MessagePacker, serializer: BinarySerializer):
        packer.pack_str(obj)

    def get_type_id(self) -> int:
        return TYPE_ID_STRING


@hana_binary_deserializer(TYPE_ID_STRING)
@memoized
@injectable_class
class StringBinaryDeserializer(TypeBinaryDeserializer[str]):
    def deserialize(self, value: Any, binary_deserializer: BinaryDeserializer) -> str:
        assert isinstance(value, str)
        return value

    def get_serialized_type(self) -> type:
        return str


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(StringReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(StringReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(StringBinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(StringBinarySerializer))
