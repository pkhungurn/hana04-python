from typing import Dict, Any

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_readable_deserializer_module, \
    hana_readable_serializer_module, hana_binary_deserializer_module, hana_binary_serializer_module
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.gfxbase.gfxtype.point3i import Point3i
from hana04.gfxbase.serialize.type_ids import TYPE_NAME_POINT3I, TYPE_ID_POINT3I
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import memoized, injectable_class


@hana_readable_serializer_by_type(Point3i)
@memoized
@injectable_class
class Point3iReadableSerializer(TypeReadableSerializer[Point3i]):
    def serialize(self, obj: Point3i, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_POINT3I,
            "value": [obj.x, obj.y, obj.z]
        }


@hana_readable_deserializer(TYPE_NAME_POINT3I)
@memoized
@injectable_class
class Point3iReadableDeserializer(TypeReadableDeserializer[Point3i]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> Point3i:
        x = json["value"][0]
        y = json["value"][1]
        z = json["value"][2]
        return Point3i(x, y, z)

    def get_serialized_type(self) -> type:
        return Point3i


@hana_binary_serializer_by_type(Point3i)
@memoized
@injectable_class
class Point3iBinarySerializer(TypeBinarySerializer[Point3i]):
    def serialize(self, obj: Point3i, packer: MessagePacker, serializer: BinarySerializer):
        packer.pack_array_header(3)
        packer.pack_int(int(obj.x))
        packer.pack_int(int(obj.y))
        packer.pack_int(int(obj.z))

    def get_type_id(self) -> int:
        return TYPE_ID_POINT3I


@hana_binary_deserializer(TYPE_ID_POINT3I)
@memoized
@injectable_class
class Point3iBinaryDeserializer(TypeBinaryDeserializer[Point3i]):
    def deserialize(self, value: Any, binary_deserializer: BinaryDeserializer) -> Point3i:
        assert isinstance(value, list)
        return Point3i(int(value[0]), int(value[1]), int(value[2]))

    def get_serialized_type(self) -> type:
        return Point3i


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(Point3iReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(Point3iReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(Point3iBinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(Point3iBinarySerializer))
