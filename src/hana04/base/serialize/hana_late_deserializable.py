from abc import abstractmethod
from typing import Dict, Any

from hana04.base.extension.hana_object import HanaObject
from hana04.base.serialize.binary.binary_deserializer import BinaryDeserializer
from hana04.base.serialize.readable.readable_deserializer import ReadableDeserializer


class HanaLateDeserializable(HanaObject):
    """
    A HanaObject with the following properties:
    (1) An instance can be created without specifying property values (i.e., all properties have default values).
    (2) All properties are Variables. This allows the object to be deserialized after it is created.
    """

    @abstractmethod
    def readable_deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer):
        pass

    @abstractmethod
    def binary_deserialize(self, value: Dict[int, Any], deserializer: BinaryDeserializer):
        pass
