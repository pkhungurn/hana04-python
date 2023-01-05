from dataclasses import dataclass
from typing import Any, Dict

from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.type_ids import TYPE_NAME_HANA_MAP_ENTRY, TYPE_ID_HANA_MAP_ENTRY
from hana04.base.util.message_packer import MessagePacker
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import memoized, injectable_class


@dataclass(frozen=True, eq=True)
class HanaMapEntry:
    key: Any
    value: Any


@memoized
@injectable_class
class HanaMapEntryReadableSerializer(TypeReadableSerializer[HanaMapEntry]):
    def serialize(self, obj: HanaMapEntry, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_HANA_MAP_ENTRY,
            "key": serializer.serialize(obj.key),
            "value": serializer.serialize(obj.value),
        }


@memoized
@injectable_class
class HanaMapEntryReadableDeserializer(TypeReadableDeserializer[HanaMapEntry]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> HanaMapEntry:
        key = deserializer.deserialize(json["key"])
        value = deserializer.deserialize(json["value"])
        return HanaMapEntry(key, value)

    def get_serialized_type(self) -> type:
        return HanaMapEntry


@memoized
@injectable_class
class HanaMapEntryBinarySerializer(TypeBinarySerializer[HanaMapEntry]):
    def serialize(self, obj: HanaMapEntry, packer: MessagePacker, serializer: BinarySerializer):
        packer.pack_array_header(2)
        serializer.serialize(obj.key)
        serializer.serialize(obj.value)

    def get_type_id(self) -> int:
        return TYPE_ID_HANA_MAP_ENTRY


@memoized
@injectable_class
class HanaMapEntryBinaryDeserializer(TypeBinaryDeserializer[HanaMapEntry]):
    def deserialize(self, value: Any, deserializer: BinaryDeserializer) -> HanaMapEntry:
        assert isinstance(value, list)
        assert isinstance(value[0], dict)
        assert isinstance(value[1], dict)
        deserialized_key = deserializer.deserialize(value[0])
        deserialized_value = deserializer.deserialize(value[1])
        return HanaMapEntry(deserialized_key, deserialized_value)

    def get_serialized_type(self) -> type:
        return HanaMapEntry


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_class(HanaMapEntryReadableSerializer)
        binder.install_module(ReadableSerializer.Module)
        binder.bind_to_dict(type, TypeReadableSerializer) \
            .with_key(HanaMapEntry) \
            .to_type(HanaMapEntryReadableSerializer)

        binder.install_class(HanaMapEntryReadableDeserializer)
        binder.install_module(ReadableDeserializer.Module)
        binder.bind_to_dict(str, TypeReadableDeserializer) \
            .with_key(TYPE_NAME_HANA_MAP_ENTRY) \
            .to_type(HanaMapEntryReadableDeserializer)

        binder.install_class(HanaMapEntryBinarySerializer)
        binder.install_module(BinarySerializer.Module)
        binder.bind_to_dict(type, TypeBinarySerializer) \
            .with_key(HanaMapEntry) \
            .to_type(HanaMapEntryBinarySerializer)

        binder.install_class(HanaMapEntryBinaryDeserializer)
        binder.install_module(BinaryDeserializer.Module)
        binder.bind_to_dict(int, TypeBinaryDeserializer) \
            .with_key(TYPE_ID_HANA_MAP_ENTRY) \
            .to_type(HanaMapEntryBinaryDeserializer)
