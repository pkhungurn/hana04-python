import typing
from dataclasses import dataclass
from typing import Any

from hana04.apt.extensible.property_type_spec import PropertyTypeSpec
from hana04.base.serialize.binary.binary_deserializer import BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import ReadableSerializer
from hana04.base.util.message_packer import MessagePacker


@dataclass(eq=True, frozen=True)
class HanaPropertySpec:
    name: str
    id: int
    type_spec: PropertyTypeSpec

    def __post_init__(self):
        assert len(self.name) > 0
        assert self.id > 0
        assert self.type_spec is not None

    @staticmethod
    def create(name: str, id: int, annotation: Any):
        return HanaPropertySpec(name, id, PropertyTypeSpec.create(annotation))

    @property
    def private_field_name(self):
        return "_" + self.name

    def add_readable_children_to_list(self,
                                      value,
                                      readable_serializer: ReadableSerializer,
                                      result: typing.List[typing.Dict[str, Any]]):
        self.type_spec.add_readable_children_to_list(value, self.name, readable_serializer, result)

    def binary_serialize_value(self, value: Any, packer: MessagePacker, serializer: BinarySerializer):
        if self.type_spec.should_binary_serialize_value(value):
            packer.pack_int(self.id)
            self.type_spec.binary_serialize_value(value, packer, serializer)

    def should_binary_serialize_value(self, value: Any):
        return self.type_spec.should_binary_serialize_value(value)

    def binary_deserialize_into_builder(self, value, builder, deserializer: BinaryDeserializer):
        self.type_spec.binary_deserialize_into_builder(self.name, value, builder, deserializer)

    def readable_deserialize_into_builder(self, value, builder, deserializer: ReadableDeserializer):
        self.type_spec.readable_deserialize_into_builder(self.name, value, builder, deserializer)

    def readable_deserialize_into_raw_data(
            self, value: typing.Dict[str, Any], raw_data, deserializer: ReadableDeserializer):
        self.type_spec.readable_deserialize_into_raw_data(self.name, value, raw_data, deserializer)

    def binary_deserialize_into_raw_data(
            self, value, raw_data, deserializer: BinaryDeserializer):
        self.type_spec.binary_deserialize_into_raw_data(self.name, value, raw_data, deserializer)
