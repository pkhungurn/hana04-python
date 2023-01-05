import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union, List, Any

from makefun import with_signature
from hana04.apt.util import capitalize_first_letter
from hana04.base.caching.wrapped import Wrapped, wrap_if_needed
from hana04.base.changeprop.variable import Variable
from hana04.base.serialize.binary.binary_deserializer import BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import ReadableSerializer
from hana04.base.util.hana_map_entry import HanaMapEntry
from hana04.base.util.message_packer import MessagePacker


class PropertyTypeSpec(ABC):
    @staticmethod
    def create(type_):
        origin = typing.get_origin(type_)
        if origin is not None:
            args = typing.get_args(type_)
        else:
            args = None
        if origin == Union:
            assert len(args) == 2
            assert args[1] == type(None)
            return OptionalTypeSpec(PropertyTypeSpec.create(args[0]))
        elif origin == Wrapped:
            assert len(args) == 1
            return WrappedTypeSpec(PropertyTypeSpec.create(args[0]))
        elif origin == list:
            assert len(args) == 1
            return ListTypeSpec(PropertyTypeSpec.create(args[0]))
        elif origin == dict:
            key_spec = PropertyTypeSpec.create(args[0])
            value_spec = PropertyTypeSpec.create(args[1])
            return DictTypeSpec(key_spec, value_spec)
        elif origin == Variable:
            assert len(args) == 1
            return VariableTypeSpec(PropertyTypeSpec.create(args[0]))
        elif origin is None:
            return TerminalTypeSpec(type_)
        else:
            raise RuntimeError(f"Cannot deal with type: {type_}")

    @abstractmethod
    def get_raw_data_class_initial_value(self):
        pass

    @abstractmethod
    def prepare_deserialized_value_for_storage(self, value):
        pass

    @abstractmethod
    def add_raw_data_builder_methods(self, builder_class, field_name: str):
        pass

    @abstractmethod
    def add_readable_children_to_list(
            self,
            value,
            field_name: str,
            readable_serializer: ReadableSerializer,
            result: List[typing.Dict[str, Any]]):
        pass

    @abstractmethod
    def should_binary_serialize_value(self, value) -> bool:
        pass

    @abstractmethod
    def binary_serialize_value(self, value, packer: MessagePacker, serializer: BinarySerializer):
        pass

    @abstractmethod
    def binary_deserialize_into_builder(self, field_name: str, value, builder, deserializer: BinaryDeserializer):
        pass

    @abstractmethod
    def readable_deserialize_into_builder(
            self, field_name: str, value: typing.Dict[str, Any], builder, deserializer: ReadableDeserializer):
        pass

    @abstractmethod
    def readable_deserialize_into_raw_data(
            self, field_name: str, value: typing.Dict[str, Any], raw_data, deserializer: ReadableDeserializer):
        pass

    @abstractmethod
    def binary_deserialize_into_raw_data(
            self, field_name: str, value, raw_data, deserializer: BinaryDeserializer):
        pass


@dataclass(eq=True, frozen=True)
class TerminalTypeSpec(PropertyTypeSpec):
    annotation: Any

    def __post_init__(self):
        assert typing.get_origin(self.annotation) is None

    def get_raw_data_class_initial_value(self):
        return None

    def prepare_deserialized_value_for_storage(self, value):
        return value

    def builder_set_method_name(self, field_name: str):
        return f"set{capitalize_first_letter(field_name)}"

    def builder_get_method_name(self, field_name: str):
        return f"get{capitalize_first_letter(field_name)}"

    def add_raw_data_builder_methods(self, builder_class, field_name: str):
        this = self

        # set method
        if True:
            set_method_name = self.builder_set_method_name(field_name)

            @with_signature(f"{set_method_name}(self, new_value)")
            def set_method(self, new_value):
                setattr(self._instance, field_name, this.prepare_deserialized_value_for_storage(new_value))
                return self

            setattr(builder_class, set_method_name, set_method)

        # get method
        if True:
            get_method_name = self.builder_get_method_name(field_name)

            @with_signature(f"{get_method_name}(self)")
            def get_method(self):
                output = getattr(self._instance, field_name)
                return output

            setattr(builder_class, get_method_name, get_method)

    def add_readable_children_to_list(
            self,
            value,
            field_name: str,
            readable_serializer: ReadableSerializer,
            result: List[typing.Dict[str, Any]]):
        result.append(readable_serializer.serialize(value, field_name))

    def should_binary_serialize_value(self, value) -> bool:
        return True

    def binary_serialize_value(self, value, packer: MessagePacker, serializer: BinarySerializer):
        serializer.serialize(value)

    def binary_deserialize_into_builder(self, field_name: str, value, builder, deserializer: BinaryDeserializer):
        assert isinstance(value, dict)
        deserialized = deserializer.deserialize(value)
        builder_method_name = self.builder_set_method_name(field_name)
        getattr(builder, builder_method_name)(deserialized)

    def readable_deserialize_into_builder(
            self, field_name: str, value: typing.Dict[str, Any], builder, deserializer: ReadableDeserializer):
        assert isinstance(value, dict)
        deserialized = deserializer.deserialize(value)
        builder_method_name = self.builder_set_method_name(field_name)
        getattr(builder, builder_method_name)(deserialized)

    def readable_deserialize_into_raw_data(
            self, field_name: str, value: typing.Dict[str, Any], raw_data, deserializer: ReadableDeserializer):
        assert isinstance(value, dict)
        deserialized = deserializer.deserialize(value)
        setattr(raw_data, field_name, deserialized)

    def binary_deserialize_into_raw_data(
            self, field_name: str, value, raw_data, deserializer: BinaryDeserializer):
        assert isinstance(value, dict)
        deserialized = deserializer.deserialize(value)
        setattr(raw_data, field_name, deserialized)


@dataclass(eq=True, frozen=True)
class WrappedTypeSpec(PropertyTypeSpec):
    inner: TerminalTypeSpec

    def __post_init__(self):
        assert isinstance(self.inner, TerminalTypeSpec)

    def get_raw_data_class_initial_value(self):
        return None

    def prepare_deserialized_value_for_storage(self, value):
        return wrap_if_needed(value)

    def builder_set_method_name(self, field_name):
        return f"set{capitalize_first_letter(field_name)}"

    def builder_get_method_name(self, field_name):
        return f"get{capitalize_first_letter(field_name)}"

    def add_raw_data_builder_methods(self, builder_class, field_name: str):
        this = self

        # set method
        if True:
            set_method_name = self.builder_set_method_name(field_name)

            @with_signature(f"{set_method_name}(self, new_value)")
            def set_method(self, new_value):
                setattr(self._instance, field_name, this.prepare_deserialized_value_for_storage(new_value))
                return self

            setattr(builder_class, set_method_name, set_method)

        # get method
        if True:
            get_method_name = self.builder_get_method_name(field_name)

            @with_signature(f"{get_method_name}(self)")
            def get_method(self):
                return getattr(self._instance, field_name)

            setattr(builder_class, get_method_name, get_method)

    def add_readable_children_to_list(
            self,
            value,
            field_name: str,
            readable_serializer: ReadableSerializer,
            result: List[typing.Dict[str, Any]]):
        assert isinstance(value, Wrapped)
        result.append(readable_serializer.serialize(value, field_name))

    def should_binary_serialize_value(self, value) -> bool:
        return True

    def binary_serialize_value(self, value, packer: MessagePacker, serializer: BinarySerializer):
        assert isinstance(value, Wrapped)
        serializer.serialize(value)

    def binary_deserialize_into_builder(self, field_name: str, value, builder, deserializer: BinaryDeserializer):
        assert isinstance(value, dict)
        deserialized = deserializer.deserialize(value)
        builder_method_name = self.builder_set_method_name(field_name)
        getattr(builder, builder_method_name)(deserialized)

    def readable_deserialize_into_builder(
            self, field_name: str, value: typing.Dict[str, Any], builder, deserializer: ReadableDeserializer):
        assert isinstance(value, dict)
        deserialized = deserializer.deserialize(value)
        builder_method_name = self.builder_set_method_name(field_name)
        getattr(builder, builder_method_name)(deserialized)

    def readable_deserialize_into_raw_data(
            self, field_name: str, value: typing.Dict[str, Any], raw_data, deserializer: ReadableDeserializer):
        assert isinstance(value, dict)
        deserialized = deserializer.deserialize(value)
        setattr(raw_data, field_name, wrap_if_needed(deserialized))

    def binary_deserialize_into_raw_data(
            self, field_name: str, value, raw_data, deserializer: BinaryDeserializer):
        assert isinstance(value, dict)
        deserialized = deserializer.deserialize(value)
        setattr(raw_data, field_name, wrap_if_needed(deserialized))


@dataclass(eq=True, frozen=True)
class OptionalTypeSpec(PropertyTypeSpec):
    inner: Union[TerminalTypeSpec, WrappedTypeSpec]

    def __post_init__(self):
        assert isinstance(self.inner, TerminalTypeSpec) or isinstance(self.inner, WrappedTypeSpec)

    def get_raw_data_class_initial_value(self):
        return None

    def prepare_deserialized_value_for_storage(self, value):
        raise AssertionError("This method should not be called on an OptionalTypeSpec")

    def builder_set_method_name(self, field_name):
        return f"set{capitalize_first_letter(field_name)}"

    def builder_get_method_name(self, field_name):
        return f"get{capitalize_first_letter(field_name)}"

    def add_raw_data_builder_methods(self, builder_class, field_name: str):
        this = self

        # set method
        if True:
            set_method_name = self.builder_set_method_name(field_name)

            @with_signature(f"{set_method_name}(self, new_value)")
            def set_method(self, new_value):
                setattr(self._instance, field_name, this.inner.prepare_deserialized_value_for_storage(new_value))
                return self

            setattr(builder_class, set_method_name, set_method)

        # get method
        if True:
            get_method_name = self.builder_get_method_name(field_name)

            @with_signature(f"{get_method_name}(self)")
            def get_method(self):
                return getattr(self._instance, field_name)

            setattr(builder_class, get_method_name, get_method)

    def add_readable_children_to_list(
            self,
            value,
            field_name: str,
            readable_serializer: ReadableSerializer,
            result: List[typing.Dict[str, Any]]):
        if value is not None:
            result.append(readable_serializer.serialize(value, field_name))

    def should_binary_serialize_value(self, value) -> bool:
        return value is not None

    def binary_serialize_value(self, value, packer: MessagePacker, serializer: BinarySerializer):
        if value is None:
            return
        serializer.serialize(value)

    def binary_deserialize_into_builder(self, field_name: str, value, builder, deserializer: BinaryDeserializer):
        assert isinstance(value, dict)
        deserialized = deserializer.deserialize(value)
        builder_method_name = self.builder_set_method_name(field_name)
        getattr(builder, builder_method_name)(deserialized)

    def readable_deserialize_into_builder(
            self, field_name: str, value: typing.Dict[str, Any], builder, deserializer: ReadableDeserializer):
        assert isinstance(value, dict)
        deserialized = deserializer.deserialize(value)
        builder_method_name = self.builder_set_method_name(field_name)
        getattr(builder, builder_method_name)(deserialized)

    def readable_deserialize_into_raw_data(
            self, field_name: str, value: typing.Dict[str, Any], raw_data, deserializer: ReadableDeserializer):
        assert isinstance(value, dict)
        deserialized = deserializer.deserialize(value)
        setattr(raw_data, field_name, self.inner.prepare_deserialized_value_for_storage(deserialized))

    def binary_deserialize_into_raw_data(
            self, field_name: str, value, raw_data, deserializer: BinaryDeserializer):
        assert isinstance(value, dict)
        deserialized = deserializer.deserialize(value)
        setattr(raw_data, field_name, self.inner.prepare_deserialized_value_for_storage(deserialized))


@dataclass(eq=True, frozen=True)
class ListTypeSpec(PropertyTypeSpec):
    inner: Union[TerminalTypeSpec, WrappedTypeSpec]

    def __post_init__(self):
        assert isinstance(self.inner, TerminalTypeSpec) or isinstance(self.inner, WrappedTypeSpec)

    def get_raw_data_class_initial_value(self):
        return []

    def prepare_deserialized_value_for_storage(self, value):
        raise AssertionError("This method should not be called on a ListTypeSpec")

    def builder_add_method_name(self, field_name):
        return f"add{capitalize_first_letter(field_name)}"

    def builder_get_method_name(self, field_name):
        return f"get{capitalize_first_letter(field_name)}"

    def builder_clear_method_name(self, field_name):
        return f"clear{capitalize_first_letter(field_name)}"

    def add_raw_data_builder_methods(self, builder_class, field_name: str):
        this = self

        # add method
        if True:
            add_method_name = self.builder_add_method_name(field_name)

            @with_signature(f"{add_method_name}(self, *new_values)")
            def add_method(self, *new_values):
                the_list = getattr(self._instance, field_name)
                for new_value in new_values:
                    the_list.append(this.inner.prepare_deserialized_value_for_storage(new_value))
                return self

            setattr(builder_class, add_method_name, add_method)

        # get method
        if True:
            get_method_name = self.builder_get_method_name(field_name)

            @with_signature(f"{add_method_name}(self)")
            def get_method(self):
                the_list = getattr(self._instance, field_name)
                return the_list

            setattr(builder_class, get_method_name, get_method)

        # clear method
        if True:
            clear_method_name = self.builder_clear_method_name(field_name)

            @with_signature(f"{clear_method_name}(self)")
            def clear_method(self):
                the_list = getattr(self._instance, field_name)
                the_list.clear()
                return self

            setattr(builder_class, clear_method_name, clear_method)

    def add_readable_children_to_list(
            self,
            value,
            field_name: str,
            readable_serializer: ReadableSerializer,
            result: List[typing.Dict[str, Any]]):
        assert isinstance(value, list)
        for item in value:
            self.inner.add_readable_children_to_list(item, field_name, readable_serializer, result)

    def should_binary_serialize_value(self, value) -> bool:
        return True

    def binary_serialize_value(self, value, packer: MessagePacker, serializer: BinarySerializer):
        assert isinstance(value, list)
        n = len(value)
        packer.pack_array_header(n)
        for item in value:
            self.inner.binary_serialize_value(item, packer, serializer)

    def binary_deserialize_into_builder(self, field_name: str, value, builder, deserializer: BinaryDeserializer):
        assert isinstance(value, list)
        builder_method_name = self.builder_add_method_name(field_name)
        builder_method = getattr(builder, builder_method_name)
        for item_value in value:
            assert isinstance(item_value, dict)
            deserialized = deserializer.deserialize(item_value)
            builder_method(deserialized)

    def readable_deserialize_into_builder(
            self, field_name: str, value: typing.Dict[str, Any], builder, deserializer: ReadableDeserializer):
        assert isinstance(value, dict)
        deserialized = deserializer.deserialize(value)
        builder_method_name = self.builder_add_method_name(field_name)
        getattr(builder, builder_method_name)(deserialized)

    def readable_deserialize_into_raw_data(
            self, field_name: str, value: typing.Dict[str, Any], raw_data, deserializer: ReadableDeserializer):
        assert isinstance(value, dict)
        the_list = getattr(raw_data, field_name)
        assert isinstance(the_list, list)
        deserialized = deserializer.deserialize(value)
        the_list.append(self.inner.prepare_deserialized_value_for_storage(deserialized))

    def binary_deserialize_into_raw_data(
            self, field_name: str, value, raw_data, deserializer: BinaryDeserializer):
        assert isinstance(value, list)
        the_list = getattr(raw_data, field_name)
        assert isinstance(the_list, list)
        for item_value in value:
            assert isinstance(item_value, dict)
            deserialized_item = deserializer.deserialize(item_value)
            the_list.append(self.inner.prepare_deserialized_value_for_storage(deserialized_item))


@dataclass(eq=True, frozen=True)
class DictTypeSpec(PropertyTypeSpec):
    key_spec: TerminalTypeSpec
    value_spec: Union[TerminalTypeSpec, WrappedTypeSpec]

    def __post_init__(self):
        assert isinstance(self.key_spec, TerminalTypeSpec)
        assert isinstance(self.value_spec, TerminalTypeSpec) or isinstance(self.value_spec, WrappedTypeSpec)

    def get_raw_data_class_initial_value(self):
        return {}

    def prepare_deserialized_value_for_storage(self, value):
        raise AssertionError("This method should not be called on a DictTypeSpec")

    def builder_put_method_name(self, field_name: str):
        return f"put{capitalize_first_letter(field_name)}"

    def builder_get_method_name(self, field_name: str):
        return f"get{capitalize_first_letter(field_name)}"

    def builder_clear_method_name(self, field_name: str):
        return f"clear{capitalize_first_letter(field_name)}"

    def builder_delete_method_name(self, field_name: str):
        return f"delete{capitalize_first_letter(field_name)}"

    def add_raw_data_builder_methods(self, builder_class, field_name: str):
        this = self

        # put method
        if True:
            put_method_name = self.builder_put_method_name(field_name)

            @with_signature(f"{put_method_name}(self, key, value)")
            def put_method(self, key, value):
                the_dict = getattr(self._instance, field_name)
                the_dict[key] = this.value_spec.prepare_deserialized_value_for_storage(value)
                return self

            setattr(builder_class, put_method_name, put_method)

        # get method
        if True:
            get_method_name = self.builder_get_method_name(field_name)

            @with_signature(f"{get_method_name}(self)")
            def get_method(self):
                the_dict = getattr(self._instance, field_name)
                return the_dict

            setattr(builder_class, get_method_name, get_method)

        # clear method
        if True:
            clear_method_name = self.builder_clear_method_name(field_name)

            @with_signature(f"{clear_method_name}(self)")
            def clear_method(self):
                the_dict = getattr(self._instance, field_name)
                the_dict.clear()
                return self

            setattr(builder_class, clear_method_name, clear_method)

        # delete method
        if True:
            delete_method_name = self.builder_delete_method_name(field_name)

            @with_signature(f"{delete_method_name}(self, key)")
            def delete_method(self, key):
                the_dict = getattr(self._instance, field_name)
                if key in the_dict:
                    del the_dict[key]
                return self

            setattr(builder_class, delete_method_name, delete_method)

    def add_readable_children_to_list(
            self,
            value,
            field_name: str,
            readable_serializer: ReadableSerializer,
            result: List[typing.Dict[str, Any]]):
        assert isinstance(value, dict)
        for key_, value_ in value.items():
            result.append(readable_serializer.serialize(HanaMapEntry(key_, value_), field_name))

    def should_binary_serialize_value(self, value) -> bool:
        return True

    def binary_serialize_value(self, value, packer: MessagePacker, serializer: BinarySerializer):
        assert isinstance(value, dict)
        n = len(value)
        packer.pack_array_header(n)
        for key_, item_ in value.items():
            serializer.serialize(HanaMapEntry(key_, item_))

    def binary_deserialize_into_builder(self, field_name: str, value, builder, deserializer: BinaryDeserializer):
        assert isinstance(value, list)
        builder_method_name = self.builder_put_method_name(field_name)
        builder_method = getattr(builder, builder_method_name)
        for item_value in value:
            assert isinstance(item_value, dict)
            deserialized = deserializer.deserialize(item_value)
            assert isinstance(deserialized, HanaMapEntry)
            builder_method(deserialized.key, deserialized.value)

    def readable_deserialize_into_builder(
            self, field_name: str, value: typing.Dict[str, Any], builder, deserializer: ReadableDeserializer):
        assert isinstance(value, dict)
        deserialized = deserializer.deserialize(value)
        assert isinstance(deserialized, HanaMapEntry)
        builder_method_name = self.builder_put_method_name(field_name)
        getattr(builder, builder_method_name)(deserialized.key, deserialized.value)

    def readable_deserialize_into_raw_data(
            self, field_name: str, value: typing.Dict[str, Any], raw_data, deserializer: ReadableDeserializer):
        assert isinstance(value, dict)
        the_dict = getattr(raw_data, field_name)
        assert isinstance(the_dict, dict)
        deserialized = deserializer.deserialize(value)
        assert isinstance(deserialized, HanaMapEntry)
        the_dict[deserialized.key] = self.value_spec.prepare_deserialized_value_for_storage(deserialized.value)

    def binary_deserialize_into_raw_data(
            self, field_name: str, value, raw_data, deserializer: BinaryDeserializer):
        assert isinstance(value, list)
        the_dict = getattr(raw_data, field_name)
        assert isinstance(the_dict, dict)
        for item_value in value:
            assert isinstance(item_value, dict)
            deserialized = deserializer.deserialize(item_value)
            assert isinstance(deserialized, HanaMapEntry)
            the_dict[deserialized.key] = self.value_spec.prepare_deserialized_value_for_storage(deserialized.value)


@dataclass(eq=True, frozen=True)
class VariableTypeSpec(PropertyTypeSpec):
    inner: PropertyTypeSpec

    def __post_init__(self):
        assert isinstance(self.inner, TerminalTypeSpec) \
               or isinstance(self.inner, WrappedTypeSpec) \
               or isinstance(self.inner, OptionalTypeSpec) \
               or isinstance(self.inner, ListTypeSpec) \
               or isinstance(self.inner, DictTypeSpec)

    def get_raw_data_class_initial_value(self):
        return self.inner.get_raw_data_class_initial_value()

    def prepare_deserialized_value_for_storage(self, value):
        raise AssertionError("This method should not be called on a VariableTypeSpec")

    def add_raw_data_builder_methods(self, builder_class, field_name: str):
        self.inner.add_raw_data_builder_methods(builder_class, field_name)

    def add_readable_children_to_list(
            self,
            value,
            field_name: str,
            readable_serializer: ReadableSerializer,
            result: List[typing.Dict[str, Any]]):
        assert isinstance(value, Variable)
        self.inner.add_readable_children_to_list(value.value(), field_name, readable_serializer, result)

    def should_binary_serialize_value(self, value) -> bool:
        assert isinstance(value, Variable)
        return self.inner.should_binary_serialize_value(value.value())

    def binary_serialize_value(self, value, packer: MessagePacker, serializer: BinarySerializer):
        return self.inner.binary_serialize_value(value.value(), packer, serializer)

    def binary_deserialize_into_builder(self, field_name: str, value, builder, deserializer: BinaryDeserializer):
        self.inner.binary_deserialize_into_builder(field_name, value, builder, deserializer)

    def readable_deserialize_into_builder(
            self, field_name: str, value: typing.Dict[str, Any], builder, deserializer: ReadableDeserializer):
        self.inner.readable_deserialize_into_builder(field_name, value, builder, deserializer)

    def readable_deserialize_into_raw_data(
            self, field_name: str, value: typing.Dict[str, Any], raw_data, deserializer: ReadableDeserializer):
        self.inner.readable_deserialize_into_raw_data(field_name, value, raw_data, deserializer)

    def binary_deserialize_into_raw_data(
            self, field_name: str, value, raw_data, deserializer: BinaryDeserializer):
        self.inner.binary_deserialize_into_raw_data(field_name, value, raw_data, deserializer)
