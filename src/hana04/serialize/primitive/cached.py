from typing import Dict, Any

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_binary_deserializer_module, \
    hana_binary_serializer_module, hana_readable_deserializer_module, hana_readable_serializer_module
from hana04.base.caching.wrapped import Direct
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.serialize.type_ids import TYPE_ID_DIRECT, TYPE_NAME_DIRECT
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import injectable_class, memoized


@hana_readable_serializer_by_type(Direct)
@memoized
@injectable_class
class DirectReadableSerializer(TypeReadableSerializer[Direct]):
    def serialize(self, obj: Direct, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_DIRECT,
            "value": serializer.serialize(obj.value),
        }


@hana_readable_deserializer(TYPE_NAME_DIRECT)
@memoized
@injectable_class
class DirectReadableDeserializer(TypeReadableDeserializer[Direct]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> Direct:
        value = deserializer.deserialize(json["value"])
        return Direct.of(value)

    def get_serialized_type(self) -> type:
        return Direct


@hana_binary_serializer_by_type(Direct)
@memoized
@injectable_class
class DirectBinarySerializer(TypeBinarySerializer[Direct]):
    def serialize(self, obj: Direct, packer: MessagePacker, serializer: BinarySerializer):
        serializer.serialize(obj.value)

    def get_type_id(self) -> int:
        return TYPE_ID_DIRECT


@hana_binary_deserializer(TYPE_ID_DIRECT)
@memoized
@injectable_class
class DirectBinaryDeserializer(TypeBinaryDeserializer[Direct]):
    def deserialize(self, value: Any, deserializer: BinaryDeserializer) -> Direct:
        assert isinstance(value, dict)
        deserialized = deserializer.deserialize(value)
        return Direct.of(deserialized)

    def get_serialized_type(self) -> type:
        return Direct


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(DirectReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(DirectReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(DirectBinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(DirectBinarySerializer))
