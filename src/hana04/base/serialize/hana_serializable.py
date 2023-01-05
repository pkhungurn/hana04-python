from abc import ABC, abstractmethod
from typing import List, Dict, Any

from hana04.base.serialize.binary.binary_serializer import BinarySerializer
from hana04.base.serialize.readable.readable_serializer import ReadableSerializer
from hana04.base.util.message_packer import MessagePacker


class HanaSerializable(ABC):
    @abstractmethod
    def get_serialized_type_name(self) -> str:
        pass

    @abstractmethod
    def get_serialized_type_id(self) -> int:
        pass

    @abstractmethod
    def get_readable_children_list(self, readable_serializer: ReadableSerializer) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def binary_serialize_content(self, packer: MessagePacker, binary_serializer: BinarySerializer):
        pass
