from typing import Dict, Any

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_readable_deserializer_module, \
    hana_readable_serializer_module, hana_binary_deserializer_module, hana_binary_serializer_module
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.gfxbase.gfxtype.vector4d import Vector4d
from hana04.gfxbase.serialize.type_ids import TYPE_NAME_VECTOR4D, TYPE_ID_VECTOR4D
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import memoized, injectable_class


@hana_readable_serializer_by_type(Vector4d)
@memoized
@injectable_class
class Vector4dReadableSerializer(TypeReadableSerializer[Vector4d]):
    def serialize(self, obj: Vector4d, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_VECTOR4D,
            "value": [obj.x, obj.y, obj.z, obj.w]
        }


@hana_readable_deserializer(TYPE_NAME_VECTOR4D)
@memoized
@injectable_class
class Vector4dReadableDeserializer(TypeReadableDeserializer[Vector4d]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> Vector4d:
        x = json["value"][0]
        y = json["value"][1]
        z = json["value"][2]
        w = json["value"][3]
        return Vector4d(x, y, z, w)

    def get_serialized_type(self) -> type:
        return Vector4d


@hana_binary_serializer_by_type(Vector4d)
@memoized
@injectable_class
class Vector4dBinarySerializer(TypeBinarySerializer[Vector4d]):
    def serialize(self, obj: Vector4d, packer: MessagePacker, serializer: BinarySerializer):
        packer.pack_array_header(4)
        packer.pack_double_float(float(obj.x))
        packer.pack_double_float(float(obj.y))
        packer.pack_double_float(float(obj.z))
        packer.pack_double_float(float(obj.w))

    def get_type_id(self) -> int:
        return TYPE_ID_VECTOR4D


@hana_binary_deserializer(TYPE_ID_VECTOR4D)
@memoized
@injectable_class
class Vector4dBinaryDeserializer(TypeBinaryDeserializer[Vector4d]):
    def deserialize(self, value: Any, binary_deserializer: BinaryDeserializer) -> Vector4d:
        assert isinstance(value, list)
        return Vector4d(float(value[0]), float(value[1]), float(value[2]), float(value[3]))

    def get_serialized_type(self) -> type:
        return Vector4d


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(Vector4dReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(Vector4dReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(Vector4dBinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(Vector4dBinarySerializer))
