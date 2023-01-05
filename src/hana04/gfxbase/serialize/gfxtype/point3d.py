from typing import Dict, Any

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_readable_deserializer_module, \
    hana_readable_serializer_module, hana_binary_deserializer_module, hana_binary_serializer_module
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.gfxbase.gfxtype.point3d import Point3d
from hana04.gfxbase.serialize.type_ids import TYPE_NAME_POINT3D, TYPE_ID_POINT3D
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import memoized, injectable_class


@hana_readable_serializer_by_type(Point3d)
@memoized
@injectable_class
class Point3dReadableSerializer(TypeReadableSerializer[Point3d]):
    def serialize(self, obj: Point3d, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_POINT3D,
            "value": [obj.x, obj.y, obj.z]
        }


def readable_parse_point3d(value: Any):
    assert isinstance(value, list)
    x = value[0]
    y = value[1]
    z = value[2]
    return Point3d(x, y, z)


@hana_readable_deserializer(TYPE_NAME_POINT3D)
@memoized
@injectable_class
class Point3dReadableDeserializer(TypeReadableDeserializer[Point3d]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> Point3d:
        return readable_parse_point3d(json["value"])

    def get_serialized_type(self) -> type:
        return Point3d


@hana_binary_serializer_by_type(Point3d)
@memoized
@injectable_class
class Point3dBinarySerializer(TypeBinarySerializer[Point3d]):
    def serialize(self, obj: Point3d, packer: MessagePacker, serializer: BinarySerializer):
        packer.pack_array_header(3)
        packer.pack_double_float(float(obj.x))
        packer.pack_double_float(float(obj.y))
        packer.pack_double_float(float(obj.z))

    def get_type_id(self) -> int:
        return TYPE_ID_POINT3D


@hana_binary_deserializer(TYPE_ID_POINT3D)
@memoized
@injectable_class
class Point3dBinaryDeserializer(TypeBinaryDeserializer[Point3d]):
    def deserialize(self, value: Any, binary_deserializer: BinaryDeserializer) -> Point3d:
        assert isinstance(value, list)
        return Point3d(float(value[0]), float(value[1]), float(value[2]))

    def get_serialized_type(self) -> type:
        return Point3d


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(Point3dReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(Point3dReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(Point3dBinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(Point3dBinarySerializer))
