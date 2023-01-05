from typing import Dict, Any, TypeVar

from hana04.base.extension.hana_extensible import HanaExtensible
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.hana_serializable import HanaSerializable
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from hana04.base.util.message_packer import MessagePacker

T = TypeVar('T', bound=HanaSerializable, contravariant=True)


class HanaSerializableReadableSerializer(TypeReadableSerializer[T]):
    def serialize(self, obj: T, serializer: ReadableSerializer) -> Dict[str, Any]:
        result = {
            "type": obj.get_serialized_type_name(),
            "children": obj.get_readable_children_list(serializer),
        }
        if isinstance(obj, HanaExtensible):
            result["extensions"] = serializer.serialize_extensions(obj)
        return result


class HanaSerializableBinarySerializer(TypeBinarySerializer[T]):
    def __init__(self, type_id: int):
        self.type_id = type_id

    def serialize(self, obj: T, packer: MessagePacker, serializer: BinarySerializer):
        obj.binary_serialize_content(packer, serializer)

    def get_type_id(self) -> int:
        return self.type_id
