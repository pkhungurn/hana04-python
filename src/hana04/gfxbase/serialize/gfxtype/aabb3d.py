from typing import Dict, Any

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_readable_deserializer_module, \
    hana_readable_serializer_module, hana_binary_deserializer_module, hana_binary_serializer_module
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.gfxbase.gfxtype.aabb3d import Aabb3d
from hana04.gfxbase.gfxtype.point3d import Point3d
from hana04.gfxbase.serialize.gfxtype.point3d import readable_parse_point3d
from hana04.gfxbase.serialize.type_ids import TYPE_NAME_AABB3D, TYPE_ID_AABB3D
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import memoized, injectable_class


def aabb3d_readable_serialized_value(obj: Aabb3d):
    return [
        obj.p_min.x, obj.p_min.y, obj.p_min.z,
        obj.p_max.x, obj.p_max.y, obj.p_max.z
    ]


@hana_readable_serializer_by_type(Aabb3d)
@memoized
@injectable_class
class Aabb3dReadableSerializer(TypeReadableSerializer[Aabb3d]):
    def serialize(self, obj: Aabb3d, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_AABB3D,
            "value": aabb3d_readable_serialized_value(obj)
        }


def readable_parse_aabb3d(json: Any) -> Aabb3d:
    if isinstance(json, list):
        return Aabb3d(
            Point3d(float(json[0]), float(json[1]), float(json[2])),
            Point3d(float(json[3]), float(json[4]), float(json[5])))
    elif isinstance(json, str):
        comps = json.split(',')
        return Aabb3d(
            Point3d(float(comps[0]), float(comps[1]), float(comps[2])),
            Point3d(float(comps[3]), float(comps[4]), float(comps[5])))
    elif isinstance(json, dict):
        assert 'pMin' in json
        assert 'pMax' in json
        p_min = readable_parse_point3d(json["pMin"])
        p_max = readable_parse_point3d(json["pMax"])
        return Aabb3d(p_min, p_max)
    else:
        raise ValueError(f"Cannot parse a Matrix4d: value = {json}")


@hana_readable_deserializer(TYPE_NAME_AABB3D)
@memoized
@injectable_class
class Aabb3dReadableDeserializer(TypeReadableDeserializer[Aabb3d]):
    def deserialize(self, json: Any, deserializer: ReadableDeserializer) -> Aabb3d:
        return readable_parse_aabb3d(json["value"])

    def get_serialized_type(self) -> type:
        return Aabb3d


@hana_binary_serializer_by_type(Aabb3d)
@memoized
@injectable_class
class Aabb3dBinarySerializer(TypeBinarySerializer[Aabb3d]):
    def serialize(self, obj: Aabb3d, packer: MessagePacker, serializer: BinarySerializer):
        packer.pack_array_header(6)
        packer.pack_double_float(obj.p_min.x)
        packer.pack_double_float(obj.p_min.y)
        packer.pack_double_float(obj.p_min.z)
        packer.pack_double_float(obj.p_max.x)
        packer.pack_double_float(obj.p_max.y)
        packer.pack_double_float(obj.p_max.z)

    def get_type_id(self) -> int:
        return TYPE_ID_AABB3D


@hana_binary_deserializer(TYPE_ID_AABB3D)
@memoized
@injectable_class
class Aabb3dBinaryDeserializer(TypeBinaryDeserializer[Aabb3d]):
    def deserialize(self, value: Any, binary_deserializer: BinaryDeserializer) -> Aabb3d:
        assert isinstance(value, list)
        assert len(value) == 6
        return Aabb3d(
            Point3d(float(value[0]), float(value[1]), float(value[2])),
            Point3d(float(value[3]), float(value[4]), float(value[5])))

    def get_serialized_type(self) -> type:
        return Aabb3d


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(Aabb3dReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(Aabb3dReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(Aabb3dBinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(Aabb3dBinarySerializer))
