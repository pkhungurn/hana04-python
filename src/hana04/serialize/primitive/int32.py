from typing import Dict, Any

import numpy

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_binary_deserializer_module, \
    hana_binary_serializer_module, hana_readable_deserializer_module, hana_readable_serializer_module
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.serialize.type_ids import TYPE_ID_INTEGER, TYPE_NAME_INTEGER
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import injectable_class, memoized


@hana_readable_serializer_by_type(numpy.int32)
@memoized
@injectable_class
class Int32ReadableSerializer(TypeReadableSerializer[numpy.int32]):
    def serialize(self, obj: numpy.int32, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_INTEGER,
            "value": int(obj)
        }


@hana_readable_deserializer(TYPE_NAME_INTEGER)
@memoized
@injectable_class
class Int32ReadableDeserializer(TypeReadableDeserializer[numpy.int32]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> numpy.int32:
        return numpy.int32(json["value"])

    def get_serialized_type(self) -> type:
        return numpy.int32


@hana_binary_serializer_by_type(numpy.int32)
@memoized
@injectable_class
class Int32BinarySerializer(TypeBinarySerializer[numpy.int32]):
    def serialize(self, obj: numpy.int32, packer: MessagePacker, serializer: BinarySerializer):
        packer.pack_int(int(obj))

    def get_type_id(self) -> int:
        return TYPE_ID_INTEGER


@hana_binary_deserializer(TYPE_ID_INTEGER)
@memoized
@injectable_class
class Int32BinaryDeserializer(TypeBinaryDeserializer[numpy.int32]):
    def deserialize(self, value: Any, binary_deserializer: BinaryDeserializer) -> numpy.int32:
        assert isinstance(value, int)
        return numpy.int32(value)

    def get_serialized_type(self) -> type:
        return numpy.int32


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(Int32ReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(Int32ReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(Int32BinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(Int32BinarySerializer))
