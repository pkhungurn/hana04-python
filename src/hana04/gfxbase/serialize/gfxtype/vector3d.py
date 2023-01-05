from typing import Dict, Any

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_readable_deserializer_module, \
    hana_readable_serializer_module, hana_binary_deserializer_module, hana_binary_serializer_module
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.gfxbase.gfxtype.vector3d import Vector3d
from hana04.gfxbase.serialize.type_ids import TYPE_NAME_VECTOR3D, TYPE_ID_VECTOR3D
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import memoized, injectable_class


@hana_readable_serializer_by_type(Vector3d)
@memoized
@injectable_class
class Vector3dReadableSerializer(TypeReadableSerializer[Vector3d]):
    def serialize(self, obj: Vector3d, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_VECTOR3D,
            "value": [obj.x, obj.y, obj.z]
        }


@hana_readable_deserializer(TYPE_NAME_VECTOR3D)
@memoized
@injectable_class
class Vector3dReadableDeserializer(TypeReadableDeserializer[Vector3d]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> Vector3d:
        x = json["value"][0]
        y = json["value"][1]
        z = json["value"][2]
        return Vector3d(x, y, z)

    def get_serialized_type(self) -> type:
        return Vector3d


@hana_binary_serializer_by_type(Vector3d)
@memoized
@injectable_class
class Vector3dBinarySerializer(TypeBinarySerializer[Vector3d]):
    def serialize(self, obj: Vector3d, packer: MessagePacker, serializer: BinarySerializer):
        packer.pack_array_header(3)
        packer.pack_double_float(float(obj.x))
        packer.pack_double_float(float(obj.y))
        packer.pack_double_float(float(obj.z))

    def get_type_id(self) -> int:
        return TYPE_ID_VECTOR3D


@hana_binary_deserializer(TYPE_ID_VECTOR3D)
@memoized
@injectable_class
class Vector3dBinaryDeserializer(TypeBinaryDeserializer[Vector3d]):
    def deserialize(self, value: Any, binary_deserializer: BinaryDeserializer) -> Vector3d:
        assert isinstance(value, list)
        return Vector3d(float(value[0]), float(value[1]), float(value[2]))

    def get_serialized_type(self) -> type:
        return Vector3d


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(Vector3dReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(Vector3dReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(Vector3dBinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(Vector3dBinarySerializer))
