from typing import Dict, Any

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_readable_deserializer_module, \
    hana_readable_serializer_module, hana_binary_deserializer_module, hana_binary_serializer_module
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.gfxbase.gfxtype.aabb2d import Aabb2d
from hana04.gfxbase.gfxtype.point2d import Point2d
from hana04.gfxbase.serialize.gfxtype.point2d import readable_parse_point2d
from hana04.gfxbase.serialize.type_ids import TYPE_NAME_AABB2D, TYPE_ID_AABB2D
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import memoized, injectable_class


def aabb2d_readable_serialized_value(obj: Aabb2d):
    return [obj.p_min.x, obj.p_min.y, obj.p_max.x, obj.p_max.y]


@hana_readable_serializer_by_type(Aabb2d)
@memoized
@injectable_class
class Aabb2dReadableSerializer(TypeReadableSerializer[Aabb2d]):
    def serialize(self, obj: Aabb2d, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_AABB2D,
            "value": aabb2d_readable_serialized_value(obj)
        }


def readable_parse_aabb2d(json: Any) -> Aabb2d:
    if isinstance(json, list):
        return Aabb2d(
            Point2d(float(json[0]), float(json[1])),
            Point2d(float(json[2]), float(json[3])))
    elif isinstance(json, str):
        comps = json.split(',')
        return Aabb2d(
            Point2d(float(comps[0]), float(comps[1])),
            Point2d(float(comps[2]), float(comps[3])))
    elif isinstance(json, dict):
        assert 'pMin' in json
        assert 'pMax' in json
        p_min = readable_parse_point2d(json["pMin"])
        p_max = readable_parse_point2d(json["pMax"])
        return Aabb2d(p_min, p_max)
    else:
        raise ValueError(f"Cannot parse a Matrix4d: value = {json}")


@hana_readable_deserializer(TYPE_NAME_AABB2D)
@memoized
@injectable_class
class Aabb2dReadableDeserializer(TypeReadableDeserializer[Aabb2d]):
    def deserialize(self, json: Any, deserializer: ReadableDeserializer) -> Aabb2d:
        return readable_parse_aabb2d(json["value"])

    def get_serialized_type(self) -> type:
        return Aabb2d


@hana_binary_serializer_by_type(Aabb2d)
@memoized
@injectable_class
class Aabb2dBinarySerializer(TypeBinarySerializer[Aabb2d]):
    def serialize(self, obj: Aabb2d, packer: MessagePacker, serializer: BinarySerializer):
        packer.pack_array_header(4)
        packer.pack_double_float(obj.p_min.x)
        packer.pack_double_float(obj.p_min.y)
        packer.pack_double_float(obj.p_max.x)
        packer.pack_double_float(obj.p_max.y)

    def get_type_id(self) -> int:
        return TYPE_ID_AABB2D


@hana_binary_deserializer(TYPE_ID_AABB2D)
@memoized
@injectable_class
class Aabb2dBinaryDeserializer(TypeBinaryDeserializer[Aabb2d]):
    def deserialize(self, value: Any, binary_deserializer: BinaryDeserializer) -> Aabb2d:
        assert isinstance(value, list)
        assert len(value) == 4
        return Aabb2d(
            Point2d(float(value[0]), float(value[1])),
            Point2d(float(value[2]), float(value[3])))

    def get_serialized_type(self) -> type:
        return Aabb2d


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(Aabb2dReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(Aabb2dReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(Aabb2dBinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(Aabb2dBinarySerializer))
