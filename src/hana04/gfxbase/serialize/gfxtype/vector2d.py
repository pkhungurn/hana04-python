from typing import Dict, Any

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_readable_deserializer_module, \
    hana_readable_serializer_module, hana_binary_deserializer_module, hana_binary_serializer_module
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.gfxbase.serialize.type_ids import TYPE_ID_VECTOR2D, TYPE_NAME_VECTOR2D
from hana04.gfxbase.gfxtype.vector2d import Vector2d
from jyuusu.constructor_resolver import memoized, injectable_class
from jyuusu.binder import Binder, Module as JyuusuModule


@hana_readable_serializer_by_type(Vector2d)
@memoized
@injectable_class
class Vector2dReadableSerializer(TypeReadableSerializer[Vector2d]):
    def serialize(self, obj: Vector2d, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_VECTOR2D,
            "value": [obj.x, obj.y]
        }


@hana_readable_deserializer(TYPE_NAME_VECTOR2D)
@memoized
@injectable_class
class Vector2dReadableDeserializer(TypeReadableDeserializer[Vector2d]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> Vector2d:
        x = json["value"][0]
        y = json["value"][1]
        return Vector2d(x, y)

    def get_serialized_type(self) -> type:
        return Vector2d


@hana_binary_serializer_by_type(Vector2d)
@memoized
@injectable_class
class Vector2dBinarySerializer(TypeBinarySerializer[Vector2d]):
    def serialize(self, obj: Vector2d, packer: MessagePacker, serializer: BinarySerializer):
        packer.pack_array_header(2)
        packer.pack_double_float(float(obj.x))
        packer.pack_double_float(float(obj.y))

    def get_type_id(self) -> int:
        return TYPE_ID_VECTOR2D


@hana_binary_deserializer(TYPE_ID_VECTOR2D)
@memoized
@injectable_class
class Vector2dBinaryDeserializer(TypeBinaryDeserializer[Vector2d]):
    def deserialize(self, value: Any, binary_deserializer: BinaryDeserializer) -> Vector2d:
        assert isinstance(value, list)
        return Vector2d(float(value[0]), float(value[1]))

    def get_serialized_type(self) -> type:
        return Vector2d


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(Vector2dReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(Vector2dReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(Vector2dBinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(Vector2dBinarySerializer))
