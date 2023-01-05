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
from hana04.serialize.type_ids import TYPE_ID_FLOAT, TYPE_NAME_FLOAT
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import injectable_class, memoized


@hana_readable_serializer_by_type(numpy.float32)
@memoized
@injectable_class
class Float32ReadableSerializer(TypeReadableSerializer[numpy.float32]):
    def serialize(self, obj: numpy.float32, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_FLOAT,
            "value": float(obj)
        }


@hana_readable_deserializer(TYPE_NAME_FLOAT)
@memoized
@injectable_class
class Float32ReadableDeserializer(TypeReadableDeserializer[numpy.float32]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> numpy.float32:
        return numpy.float32(json["value"])

    def get_serialized_type(self) -> type:
        return numpy.float32


@hana_binary_serializer_by_type(numpy.float32)
@memoized
@injectable_class
class Float32BinarySerializer(TypeBinarySerializer[numpy.float32]):
    def serialize(self, obj: numpy.float32, packer: MessagePacker, serializer: BinarySerializer):
        packer.pack_double_float(float(obj))

    def get_type_id(self) -> int:
        return TYPE_ID_FLOAT


@hana_binary_deserializer(TYPE_ID_FLOAT)
@memoized
@injectable_class
class Float32BinaryDeserializer(TypeBinaryDeserializer[numpy.float32]):
    def deserialize(self, value: Dict[int, Any], binary_deserializer: BinaryDeserializer) -> numpy.float32:
        assert isinstance(value, float)
        return numpy.float32(value)

    def get_serialized_type(self) -> type:
        return numpy.float32


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(Float32ReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(Float32ReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(Float32BinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(Float32BinarySerializer))
