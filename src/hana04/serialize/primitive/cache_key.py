from typing import Dict, Any, List

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_binary_deserializer_module, \
    hana_binary_serializer_module, hana_readable_deserializer_module, hana_readable_serializer_module
from hana04.base.caching.cache_key import CacheKey, StringCacheKeyPart, FilePathCacheKeyPart
from hana04.base.filesystem.file_path import FilePath
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.serialize.type_ids import TYPE_ID_CACHE_KEY, TYPE_NAME_CACHE_KEY
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import injectable_class, memoized


@hana_readable_serializer_by_type(CacheKey)
@memoized
@injectable_class
class CacheKeyReadableSerializer(TypeReadableSerializer[CacheKey]):
    def serialize(self, obj: CacheKey, serializer: ReadableSerializer) -> Dict[str, Any]:
        parts = []
        for part in obj.parts:
            if isinstance(part, StringCacheKeyPart):
                parts.append(part.value)
            elif isinstance(part, FilePathCacheKeyPart):
                parts.append(serializer.serialize(part.value))
            else:
                raise RuntimeError(f"Unsupport part type {type(part)}")
        return {
            "type": TYPE_NAME_CACHE_KEY,
            "protocol": obj.protocol,
            "parts": parts
        }


@hana_readable_deserializer(TYPE_NAME_CACHE_KEY)
@memoized
@injectable_class
class CacheKeyReadableDeserializer(TypeReadableDeserializer[CacheKey]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> CacheKey:
        builder = CacheKey.Builder(json["protocol"])
        for part in json["parts"]:
            if isinstance(part, str):
                builder.add_string_part(part)
            else:
                file_path = deserializer.deserialize(part)
                assert isinstance(file_path, FilePath)
                builder.add_file_path_part(file_path)
        return builder.build()

    def get_serialized_type(self) -> type:
        return CacheKey


@hana_binary_serializer_by_type(CacheKey)
@memoized
@injectable_class
class CacheKeyBinarySerializer(TypeBinarySerializer[CacheKey]):
    def serialize(self, obj: CacheKey, packer: MessagePacker, serializer: BinarySerializer):
        packer.pack_array_header(2)
        packer.pack_str(obj.protocol)
        packer.pack_array_header(len(obj.parts))
        for part in obj.parts:
            if isinstance(part, StringCacheKeyPart):
                serializer.serialize(part.value)
            elif isinstance(part, FilePathCacheKeyPart):
                serializer.serialize(part.value)
            else:
                raise RuntimeError(f"Unsupported part type {type(part)}")

    def get_type_id(self) -> int:
        return TYPE_ID_CACHE_KEY


@hana_binary_deserializer(TYPE_ID_CACHE_KEY)
@memoized
@injectable_class
class CacheKeyBinaryDeserializer(TypeBinaryDeserializer[CacheKey]):
    def deserialize(self, value: Any, deserializer: BinaryDeserializer) -> CacheKey:
        assert isinstance(value, list)
        array: List = value
        protocol = array[0]
        parts = array[1]
        builder = CacheKey.Builder(protocol)
        for part in parts:
            deserialized_part = deserializer.deserialize(part)
            if isinstance(deserialized_part, str):
                builder.add_string_part(deserialized_part)
            elif isinstance(deserialized_part, FilePath):
                builder.add_file_path_part(deserialized_part)
            else:
                raise RuntimeError(f"Unsupported part type {type(deserialized_part)}")
        return builder.build()

    def get_serialized_type(self) -> type:
        return CacheKey


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(CacheKeyReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(CacheKeyReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(CacheKeyBinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(CacheKeyBinarySerializer))
