from typing import Dict, Any

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_readable_deserializer_module, \
    hana_readable_serializer_module, hana_binary_deserializer_module, hana_binary_serializer_module
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.gfxbase.gfxtype.transform import Transform
from hana04.gfxbase.serialize.gfxtype.matrix4d import matrix4d_readable_serialized_value, readable_parse_matrix4d, \
    pack_matrix4d, unpack_matrix4d
from hana04.gfxbase.serialize.type_ids import TYPE_ID_TRANSFORM, TYPE_NAME_TRANSFORM
from jyuusu.constructor_resolver import memoized, injectable_class
from jyuusu.binder import Binder, Module as JyuusuModule


@hana_readable_serializer_by_type(Transform)
@memoized
@injectable_class
class TransformReadableSerializer(TypeReadableSerializer[Transform]):
    def serialize(self, obj: Transform, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_TRANSFORM,
            "value": matrix4d_readable_serialized_value(obj.m)
        }


@hana_readable_deserializer(TYPE_NAME_TRANSFORM)
@memoized
@injectable_class
class TransformReadableDeserializer(TypeReadableDeserializer[Transform]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> Transform:
        m = readable_parse_matrix4d(json["value"])
        return Transform(m)

    def get_serialized_type(self) -> type:
        return Transform


@hana_binary_serializer_by_type(Transform)
@memoized
@injectable_class
class TransformBinarySerializer(TypeBinarySerializer[Transform]):
    def serialize(self, obj: Transform, packer: MessagePacker, serializer: BinarySerializer):
        pack_matrix4d(obj.m, packer)

    def get_type_id(self) -> int:
        return TYPE_ID_TRANSFORM


@hana_binary_deserializer(TYPE_ID_TRANSFORM)
@memoized
@injectable_class
class TransformBinaryDeserializer(TypeBinaryDeserializer[Transform]):
    def deserialize(self, value: Any, binary_deserializer: BinaryDeserializer) -> Transform:
        m = unpack_matrix4d(value)
        return Transform(m)

    def get_serialized_type(self) -> type:
        return Transform


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(TransformReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(TransformReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(TransformBinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(TransformBinarySerializer))
