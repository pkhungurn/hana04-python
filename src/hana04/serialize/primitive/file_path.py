from typing import Dict, Any, List

from hana04.apt.serialize.decorators import hana_readable_serializer_by_type, hana_readable_deserializer, \
    hana_binary_serializer_by_type, hana_binary_deserializer, hana_binary_deserializer_module, \
    hana_binary_serializer_module, hana_readable_deserializer_module, hana_readable_serializer_module
from hana04.base.filesystem.file_path import FilePath
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from hana04.serialize.type_ids import TYPE_ID_FILE_PATH, TYPE_NAME_FILE_PATH
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import injectable_class, memoized


@hana_readable_serializer_by_type(FilePath)
@memoized
@injectable_class
class FilePathReadableSerializer(TypeReadableSerializer[FilePath]):
    def serialize(self, obj: FilePath, serializer: ReadableSerializer) -> Dict[str, Any]:
        return {
            "type": TYPE_NAME_FILE_PATH,
            "relative": obj.save_as_relative,
            "value": obj.get_serialized_path(serializer.file_name)
        }


@hana_readable_deserializer(TYPE_NAME_FILE_PATH)
@memoized
@injectable_class
class FilePathReadableDeserializer(TypeReadableDeserializer[FilePath]):
    def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer) -> FilePath:
        relative = json["relative"]
        raw_path = str(json["value"])
        if relative:
            path_to_store = FilePath.compute_path_to_store(raw_path, deserializer.file_name)
        else:
            path_to_store = raw_path
        return FilePath(relative, path_to_store)

    def get_serialized_type(self) -> type:
        return FilePath


@hana_binary_serializer_by_type(FilePath)
@memoized
@injectable_class
class FilePathBinarySerializer(TypeBinarySerializer[FilePath]):
    def serialize(self, obj: FilePath, packer: MessagePacker, serializer: BinarySerializer):
        packer.pack_array_header(2)
        packer.pack_bool(obj.save_as_relative)
        packer.pack_str(obj.get_serialized_path(serializer.file_name))

    def get_type_id(self) -> int:
        return TYPE_ID_FILE_PATH


@hana_binary_deserializer(TYPE_ID_FILE_PATH)
@memoized
@injectable_class
class FilePathBinaryDeserializer(TypeBinaryDeserializer[FilePath]):
    def deserialize(self, value: Any, deserializer: BinaryDeserializer) -> FilePath:
        assert isinstance(value, list)
        array: List = value
        relative = array[0]
        raw_path = str(array[1])
        if relative:
            path_to_store = FilePath.compute_path_to_store(raw_path, deserializer.file_name)
        else:
            path_to_store = raw_path
        return FilePath(relative, path_to_store)

    def get_serialized_type(self) -> type:
        return FilePath


class Module(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana_readable_deserializer_module(FilePathReadableDeserializer))
        binder.install_module(hana_readable_serializer_module(FilePathReadableSerializer))
        binder.install_module(hana_binary_deserializer_module(FilePathBinaryDeserializer))
        binder.install_module(hana_binary_serializer_module(FilePathBinarySerializer))
