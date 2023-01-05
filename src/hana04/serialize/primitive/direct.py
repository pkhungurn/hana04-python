from typing import Dict, Any

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_binary_deserializer_module, \
    hana_binary_serializer_module, hana_readable_deserializer_module, hana_readable_serializer_module
from hana04.base.caching.wrapped import Cached
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.serialize.type_ids import TYPE_ID_CACHED, TYPE_NAME_CACHED
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import injectable_class, memoized


@hana_readable_serializer_by_type(Cached)
@memoized
@injectable_class
class CachedReadableSerializer(TypeReadableSerializer[Cached]):
    def serialize(self, obj: Cached, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_CACHED,
            "value": serializer.serialize(obj.key),
        }


@hana_readable_deserializer(TYPE_NAME_CACHED)
@memoized
@injectable_class
class CachedReadableDeserializer(TypeReadableDeserializer[Cached]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> Cached:
        value = deserializer.deserialize(json["value"])
        return Cached.of(value)

    def get_serialized_type(self) -> type:
        return Cached


@hana_binary_serializer_by_type(Cached)
@memoized
@injectable_class
class CachedBinarySerializer(TypeBinarySerializer[Cached]):
    def serialize(self, obj: Cached, packer: MessagePacker, serializer: BinarySerializer):
        serializer.serialize(obj.key)

    def get_type_id(self) -> int:
        return TYPE_ID_CACHED


@hana_binary_deserializer(TYPE_ID_CACHED)
@memoized
@injectable_class
class CachedBinaryDeserializer(TypeBinaryDeserializer[Cached]):
    def deserialize(self, value: Any, deserializer: BinaryDeserializer) -> Cached:
        assert isinstance(value, dict)
        deserialized = deserializer.deserialize(value)
        return Cached.of(deserialized)

    def get_serialized_type(self) -> type:
        return Cached


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(CachedReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(CachedReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(CachedBinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(CachedBinarySerializer))
