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
from hana04.serialize.type_ids import TYPE_ID_DOUBLE, TYPE_NAME_DOUBLE
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import injectable_class, memoized


@hana_readable_serializer_by_type(numpy.float64)
@memoized
@injectable_class
class Float64ReadableSerializer(TypeReadableSerializer[numpy.float64]):
    def serialize(self, obj: numpy.float64, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_DOUBLE,
            "value": float(obj)
        }


@hana_readable_deserializer(TYPE_NAME_DOUBLE)
@memoized
@injectable_class
class Float64ReadableDeserializer(TypeReadableDeserializer[numpy.float64]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> numpy.float64:
        return numpy.float64(json["value"])

    def get_serialized_type(self) -> type:
        return numpy.float64


@hana_binary_serializer_by_type(numpy.float64)
@memoized
@injectable_class
class Float64BinarySerializer(TypeBinarySerializer[numpy.float64]):
    def serialize(self, obj: numpy.float64, packer: MessagePacker, serializer: BinarySerializer):
        packer.pack_single_float(float(obj))

    def get_type_id(self) -> int:
        return TYPE_ID_DOUBLE


@hana_binary_deserializer(TYPE_ID_DOUBLE)
@memoized
@injectable_class
class Float64BinaryDeserializer(TypeBinaryDeserializer[numpy.float64]):
    def deserialize(self, value: Any, binary_deserializer: BinaryDeserializer) -> numpy.float64:
        assert isinstance(value, float)
        return numpy.float64(value)

    def get_serialized_type(self) -> type:
        return numpy.float64


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(Float64ReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(Float64ReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(Float64BinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(Float64BinarySerializer))
