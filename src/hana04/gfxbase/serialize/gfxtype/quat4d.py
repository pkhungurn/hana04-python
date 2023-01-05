from typing import Dict, Any

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_readable_deserializer_module, \
    hana_readable_serializer_module, hana_binary_deserializer_module, hana_binary_serializer_module
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.gfxbase.gfxtype.quat4d import Quat4d
from hana04.gfxbase.serialize.type_ids import TYPE_NAME_QUAT4D, TYPE_ID_QUAT4D
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import memoized, injectable_class


@hana_readable_serializer_by_type(Quat4d)
@memoized
@injectable_class
class Quat4dReadableSerializer(TypeReadableSerializer[Quat4d]):
    def serialize(self, obj: Quat4d, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_QUAT4D,
            "value": [obj.x, obj.y, obj.z, obj.w]
        }


@hana_readable_deserializer(TYPE_NAME_QUAT4D)
@memoized
@injectable_class
class Quat4dReadableDeserializer(TypeReadableDeserializer[Quat4d]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> Quat4d:
        x = json["value"][0]
        y = json["value"][1]
        z = json["value"][2]
        w = json["value"][3]
        return Quat4d(w, x, y, z)

    def get_serialized_type(self) -> type:
        return Quat4d


@hana_binary_serializer_by_type(Quat4d)
@memoized
@injectable_class
class Quat4dBinarySerializer(TypeBinarySerializer[Quat4d]):
    def serialize(self, obj: Quat4d, packer: MessagePacker, serializer: BinarySerializer):
        packer.pack_array_header(4)
        packer.pack_double_float(float(obj.x))
        packer.pack_double_float(float(obj.y))
        packer.pack_double_float(float(obj.z))
        packer.pack_double_float(float(obj.w))

    def get_type_id(self) -> int:
        return TYPE_ID_QUAT4D


@hana_binary_deserializer(TYPE_ID_QUAT4D)
@memoized
@injectable_class
class Quat4dBinaryDeserializer(TypeBinaryDeserializer[Quat4d]):
    def deserialize(self, value: Any, binary_deserializer: BinaryDeserializer) -> Quat4d:
        assert isinstance(value, list)
        return Quat4d(float(value[3]), float(value[0]), float(value[1]), float(value[2]))

    def get_serialized_type(self) -> type:
        return Quat4d


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(Quat4dReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(Quat4dReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(Quat4dBinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(Quat4dBinarySerializer))
