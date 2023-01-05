from typing import Dict, Any

import numpy

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_readable_deserializer_module, \
    hana_readable_serializer_module, hana_binary_deserializer_module, hana_binary_serializer_module
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.gfxbase.gfxtype.matrix4d import Matrix4d
from hana04.gfxbase.serialize.type_ids import TYPE_NAME_MATRIX4D, TYPE_ID_MATRIX4D
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import memoized, injectable_class


def matrix4d_readable_serialized_value(obj: Matrix4d):
    return [
        [obj[0, 0], obj[0, 1], obj[0, 2], obj[0, 3]],
        [obj[1, 0], obj[1, 1], obj[1, 2], obj[1, 3]],
        [obj[2, 0], obj[2, 1], obj[2, 2], obj[2, 3]],
        [obj[3, 0], obj[3, 1], obj[3, 2], obj[3, 3]]
    ]


@hana_readable_serializer_by_type(Matrix4d)
@memoized
@injectable_class
class Matrix4dReadableSerializer(TypeReadableSerializer[Matrix4d]):
    def serialize(self, obj: Matrix4d, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_MATRIX4D,
            "value": matrix4d_readable_serialized_value(obj)
        }


def readable_parse_matrix4d(json: Any) -> Matrix4d:
    assert isinstance(json, list)
    data = numpy.zeros((4, 4), dtype=numpy.float64)
    if len(json) == 4:
        for i in range(4):
            assert isinstance(json[i], list)
        for i in range(4):
            for j in range(4):
                data[i, j] = float(json[i][j])
    else:
        assert len(json) == 16
        for i in range(4):
            for j in range(4):
                data[i, j] = float(json[i * 4 + j])
    return Matrix4d(data, copy=False)


@hana_readable_deserializer(TYPE_NAME_MATRIX4D)
@memoized
@injectable_class
class Matrix4dReadableDeserializer(TypeReadableDeserializer[Matrix4d]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> Matrix4d:
        return readable_parse_matrix4d(json["value"])

    def get_serialized_type(self) -> type:
        return Matrix4d


def pack_matrix4d(obj: Matrix4d, packer: MessagePacker):
    packer.pack_array_header(16)
    for i in range(4):
        for j in range(4):
            packer.pack_double_float(float(obj[i, j]))


@hana_binary_serializer_by_type(Matrix4d)
@memoized
@injectable_class
class Matrix4dBinarySerializer(TypeBinarySerializer[Matrix4d]):
    def serialize(self, obj: Matrix4d, packer: MessagePacker, serializer: BinarySerializer):
        pack_matrix4d(obj, packer)

    def get_type_id(self) -> int:
        return TYPE_ID_MATRIX4D


def unpack_matrix4d(value: Any) -> Matrix4d:
    assert isinstance(value, list)
    assert len(value) == 16
    data = numpy.zeros((4, 4), dtype=numpy.float64)
    for i in range(4):
        for j in range(4):
            data[i, j] = float(value[i * 4 + j])
    return Matrix4d(data, copy=False)


@hana_binary_deserializer(TYPE_ID_MATRIX4D)
@memoized
@injectable_class
class Matrix4dBinaryDeserializer(TypeBinaryDeserializer[Matrix4d]):
    def deserialize(self, value: Any, binary_deserializer: BinaryDeserializer) -> Matrix4d:
        return unpack_matrix4d(value)

    def get_serialized_type(self) -> type:
        return Matrix4d


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(Matrix4dReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(Matrix4dReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(Matrix4dBinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(Matrix4dBinarySerializer))
