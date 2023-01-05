from typing import Dict, Any

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_readable_deserializer_module, \
    hana_readable_serializer_module, hana_binary_deserializer_module, hana_binary_serializer_module
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.gfxbase.gfxtype.point2d import Point2d
from hana04.gfxbase.serialize.type_ids import TYPE_NAME_POINT2D, TYPE_ID_POINT2D
from jyuusu.constructor_resolver import memoized, injectable_class
from jyuusu.binder import Binder, Module as JyuusuModule


@hana_readable_serializer_by_type(Point2d)
@memoized
@injectable_class
class Point2dReadableSerializer(TypeReadableSerializer[Point2d]):
    def serialize(self, obj: Point2d, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_POINT2D,
            "value": [obj.x, obj.y]
        }


def readable_parse_point2d(value: Any):
    assert isinstance(value, list)
    x = value[0]
    y = value[1]
    return Point2d(x, y)


@hana_readable_deserializer(TYPE_NAME_POINT2D)
@memoized
@injectable_class
class Point2dReadableDeserializer(TypeReadableDeserializer[Point2d]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> Point2d:
        return readable_parse_point2d(json["value"])

    def get_serialized_type(self) -> type:
        return Point2d


@hana_binary_serializer_by_type(Point2d)
@memoized
@injectable_class
class Point2dBinarySerializer(TypeBinarySerializer[Point2d]):
    def serialize(self, obj: Point2d, packer: MessagePacker, serializer: BinarySerializer):
        packer.pack_array_header(2)
        packer.pack_double_float(float(obj.x))
        packer.pack_double_float(float(obj.y))

    def get_type_id(self) -> int:
        return TYPE_ID_POINT2D


@hana_binary_deserializer(TYPE_ID_POINT2D)
@memoized
@injectable_class
class Point2dBinaryDeserializer(TypeBinaryDeserializer[Point2d]):
    def deserialize(self, value: Any, binary_deserializer: BinaryDeserializer) -> Point2d:
        assert isinstance(value, list)
        return Point2d(float(value[0]), float(value[1]))

    def get_serialized_type(self) -> type:
        return Point2d


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(Point2dReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(Point2dReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(Point2dBinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(Point2dBinarySerializer))
