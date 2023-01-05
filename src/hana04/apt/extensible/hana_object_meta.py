import typing
from typing import List, Any, Dict

from makefun import with_signature

from hana04.apt.extensible.constants import HANA_META_PROPERTY_NAME
from hana04.apt.extensible.hana_meta import HanaMeta, hana_meta
from hana04.apt.extensible.hana_property_spec import HanaPropertySpec
from hana04.apt.extensible.property_type_spec import VariableTypeSpec
from hana04.apt.serialize.decorators import hana_binary_serializer_by_type_id, hana_binary_serializer_module, \
    hana_readable_serializer_by_type_name, hana_readable_serializer_module, hana_binary_deserializer, \
    hana_binary_deserializer_module, hana_readable_deserializer, hana_readable_deserializer_module
from hana04.base.changeprop.variable import Variable
from hana04.base.extension.extensions.validator import Validator
from hana04.base.extension.fluent_builder import FluentBuilder
from hana04.base.extension.hana_customized_builders import HanaCustomizedBuilders
from hana04.base.extension.hana_extensible import HanaExtensible
from hana04.base.extension.hana_extension_manager import HanaExtensionManager
from hana04.base.extension.hana_extension_uber_factory import HanaExtensionUberFactory
from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import BinarySerializer
from hana04.base.serialize.binary.constants import EXTENSION_TAG
from hana04.base.serialize.hana_serializable_serializers import HanaSerializableBinarySerializer, \
    HanaSerializableReadableSerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import ReadableSerializer
from hana04.base.util.message_packer import MessagePacker
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import memoized, injectable_class, injectable_class_with_specs, ResolverSpec
from jyuusu.factory_resolver import injectable_factory, factory_class
from jyuusu.provider import Provider


class HanaObjectMeta(HanaMeta):
    def __init__(self, type_id: int, type_names: List[str]):
        super().__init__()
        self._type_names = type_names
        self._type_id = type_id
        self._properties: List[HanaPropertySpec] = []
        self._property_by_id: typing.Dict[int, HanaPropertySpec] = {}
        self._property_by_name: typing.Dict[str, HanaPropertySpec] = {}
        self._raw_data_class = None
        self._impl_class = None
        self._default_builder_class = None
        self._readable_serializer_class = None
        self._readable_deserializer_class = None
        self._binary_serializer_class = None
        self._binary_deserializer_class = None
        self._object_module_class = None

    @property
    def type_id(self):
        return self._type_id

    @property
    def type_names(self):
        return self._type_names

    @property
    def primary_type_name(self):
        return self._type_names[0]

    @property
    def properties(self) -> List[HanaPropertySpec]:
        return self._properties

    @property
    def raw_data_class(self):
        return self._raw_data_class

    @property
    def impl_class(self):
        return self._impl_class

    @property
    def impl_factory_class(self):
        return factory_class(self._impl_class)

    @property
    def default_builder_class(self):
        return self._default_builder_class

    @property
    def binary_serializer_class(self):
        return self._binary_serializer_class

    @property
    def binary_deserializer_class(self):
        return self._binary_deserializer_class

    @property
    def readable_serializer_class(self):
        return self._readable_serializer_class

    @property
    def readable_deserializer_class(self):
        return self._readable_deserializer_class

    @property
    def object_module_class(self):
        return self._object_module_class

    @property
    def module(self):
        return self.object_module_class

    @staticmethod
    def assert_hana_object_can_be_created(cls: type):
        HanaMeta.assert_hana_interface_can_be_created(cls)
        assert isinstance(cls.__dict__[HANA_META_PROPERTY_NAME], HanaObjectMeta)

    def add_property(self, new_property: HanaPropertySpec):
        assert new_property.id not in self._property_by_id
        assert new_property.name not in self._property_by_name
        self._properties.append(new_property)
        self._property_by_id[new_property.id] = new_property
        self._property_by_name[new_property.name] = new_property

    def make_hana_object(self, cls):
        assert cls.__dict__[HANA_META_PROPERTY_NAME] == self
        self.make_hana_interface(cls)
        self._raw_data_class = self.create_raw_data_class()
        self._impl_class = self.create_impl_class(cls)
        self._default_builder_class = self.create_default_builder_class(cls)
        self._binary_serializer_class = self.create_binary_serializer_class(cls)
        self._readable_serializer_class = self.create_readable_serializer(cls)
        self._binary_deserializer_class = self.create_binary_deserializer(cls)
        self._readable_deserializer_class = self.create_readable_deserializer(cls)
        self._object_module_class = self.create_object_module_class()

    def create_raw_data_class(self):
        hana_object_meta = self

        class _RawData:
            def __init__(self):
                for property in hana_object_meta.properties:
                    setattr(self, property.name, property.type_spec.get_raw_data_class_initial_value())

        return _RawData

    def create_hana_object_member_dict(self, cls):
        hana_object_meta = self

        def __init__(self, raw_data, extension_uber_factory: HanaExtensionUberFactory):
            self.__extension_manager = HanaExtensionManager(cls, extension_uber_factory)

            for property_ in hana_object_meta.properties:
                if isinstance(property_.type_spec, VariableTypeSpec):
                    setattr(self, property_.private_field_name, Variable(getattr(raw_data, property_.name)))
                else:
                    setattr(self, property_.private_field_name, getattr(raw_data, property_.name))

        def supports_extension(self, klass: type) -> bool:
            return self.__extension_manager.supports_extension(klass)

        def get_extension(self, klass: type):
            return self.__extension_manager.get_extension(self, klass)

        def create_extension(self, klass: type):
            return self.__extension_manager.create_extension(self, klass)

        def prepare_extension(self, klass: type):
            self.__extension_manager.prepare_extension(self, klass)

        def get_extensions(self) -> typing.Iterable[Any]:
            return self.__extension_manager.get_extensions()

        def has_extension(self, klass: type) -> bool:
            return self.__extension_manager.has_extension(klass)

        def get_serialized_type_name(self) -> str:
            return hana_object_meta.primary_type_name

        def get_serialized_type_id(self) -> int:
            return hana_object_meta.type_id

        def get_readable_children_list(self, readable_serializer: ReadableSerializer) \
                -> List[typing.Dict[str, Any]]:
            result = []
            for property_ in hana_object_meta.properties:
                property_.add_readable_children_to_list(
                    value=getattr(self, property_.private_field_name),
                    readable_serializer=readable_serializer,
                    result=result)
            return result

        def binary_serialize_content(self, packer: MessagePacker, binary_serializer: BinarySerializer):
            map_size = 1
            for property_ in hana_object_meta.properties:
                value = getattr(self, property_.private_field_name)
                if property_.should_binary_serialize_value(value):
                    map_size += 1
            packer.pack_map_header(map_size)
            for property_ in hana_object_meta.properties:
                value = getattr(self, property_.private_field_name)
                property_.binary_serialize_value(value, packer, binary_serializer)

            packer.pack_int(EXTENSION_TAG)
            binary_serializer.serialize_extensions(self)

        members = {
            "__init__": __init__,
            "supports_extension": supports_extension,
            "get_extension": get_extension,
            "has_extension": has_extension,
            "create_extension": create_extension,
            "prepare_extension": prepare_extension,
            "get_extensions": get_extensions,
            "get_serialized_type_name": get_serialized_type_name,
            "get_serialized_type_id": get_serialized_type_id,
            "get_readable_children_list": get_readable_children_list,
            "binary_serialize_content": binary_serialize_content,
        }
        for property_ in self.properties:
            members[property_.name] = self.create_property_method(property_.name, property_.private_field_name)

        return members

    def create_impl_class(self, cls):
        members = self.create_hana_object_member_dict(cls)
        _Impl = type("_Impl", (cls,), members)
        _Impl = injectable_factory("extension_uber_factory")(_Impl)
        return _Impl

    def create_default_builder_class(self, cls):
        hana_object_meta = self

        @injectable_class_with_specs(impl_factory=ResolverSpec.of(factory_class(hana_object_meta.impl_class)))
        class _DefaultBuilder(FluentBuilder[cls]):
            def __init__(self, impl_factory):
                self._impl_factory = impl_factory
                self._instance = hana_object_meta._raw_data_class()

            def build(self) -> cls:
                instance: HanaExtensible = self._impl_factory.create(self._instance)
                if instance.supports_extension(Validator):
                    validator: Validator = instance.get_extension(Validator)
                    validator.validate()
                return instance

        for property in self.properties:
            property.type_spec.add_raw_data_builder_methods(_DefaultBuilder, property.name)

        return _DefaultBuilder

    def create_property_method(self, property_name: str, private_field_name: str):
        @with_signature(f"{property_name}(self)")
        def prop(self):
            return getattr(self, private_field_name)

        return prop

    def create_binary_serializer_class(self, cls):
        hana_object_meta = self

        @hana_binary_serializer_by_type_id(hana_object_meta.type_id)
        @memoized
        @injectable_class
        class _HanaBinarySerializer(HanaSerializableBinarySerializer[cls]):
            def __init__(self):
                super().__init__(hana_object_meta.type_id)

        return _HanaBinarySerializer

    def create_readable_serializer(self, cls):
        hana_object_meta = self

        @hana_readable_serializer_by_type_name(*hana_object_meta.type_names)
        @memoized
        @injectable_class
        class _HanaReadableSerializer(HanaSerializableReadableSerializer[cls]):
            def __init__(self):
                super().__init__()

        return _HanaReadableSerializer

    def create_binary_deserializer(self, cls):
        hana_object_meta = self

        @hana_binary_deserializer(hana_object_meta.type_id)
        @memoized
        @injectable_class
        class _HanaBinaryDeserializer(TypeBinaryDeserializer[cls]):
            def __init__(self,
                         default_builder_provider: Provider[hana_object_meta.default_builder_class],
                         customized_builders: HanaCustomizedBuilders):
                self.default_builder_provider = default_builder_provider
                self.customized_builders = customized_builders

            def deserialize(self, value: Any, binary_deserializer: BinaryDeserializer) -> cls:
                assert isinstance(value, dict)

                customized_builder_factory = self.customized_builders.get_factory(cls)
                builder: FluentBuilder
                if customized_builder_factory is None:
                    builder = self.default_builder_provider.get()
                else:
                    builder = customized_builder_factory.create()

                for key_, value_ in value.items():
                    assert isinstance(key_, int)
                    if key_ not in hana_object_meta._property_by_id:
                        continue
                    property_spec = hana_object_meta._property_by_id[key_]
                    property_spec.binary_deserialize_into_builder(value_, builder, binary_deserializer)

                instance = builder.build()
                binary_deserializer.deserialize_extensions(value, instance)
                return instance

            def get_serialized_type(self) -> type:
                return cls

        return _HanaBinaryDeserializer

    @staticmethod
    def valid_json_children(json: Dict[str, Any], hana_object_meta: 'HanaObjectMeta'):
        if "children" not in json:
            return
        children = json["children"]
        assert isinstance(children, list)
        for child in children:
            assert isinstance(child, dict)
            if not "func" in child:
                continue
            func = child["func"]
            if func not in hana_object_meta._property_by_name:
                continue
            yield child

    def create_readable_deserializer(self, cls):
        hana_object_meta = self

        @hana_readable_deserializer(*hana_object_meta.type_names)
        @memoized
        @injectable_class
        class _HanaReadableDeserializer(TypeReadableDeserializer[cls]):
            def __init__(self,
                         default_builder_provider: Provider[hana_object_meta.default_builder_class],
                         customized_builders: HanaCustomizedBuilders):
                self.default_builder_provider = default_builder_provider
                self.customized_builders = customized_builders

            def deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer):
                customized_builder_factory = self.customized_builders.get_factory(cls)
                builder: FluentBuilder
                if customized_builder_factory is None:
                    builder = self.default_builder_provider.get()
                else:
                    builder = customized_builder_factory.create()

                for child in HanaObjectMeta.valid_json_children(json, hana_object_meta):
                    property_ = hana_object_meta._property_by_name[child["func"]]
                    property_.readable_deserialize_into_builder(child, builder, deserializer)

                instance = builder.build()
                deserializer.deserialize_extensions(json, instance)
                return instance

            def get_serialized_type(self) -> type:
                return cls

        return _HanaReadableDeserializer

    def create_object_module_class(self):
        hana_object_meta = self

        class _HanaObjectModule(JyuusuModule):
            def configure(self, binder: Binder):
                binder.install_module(hana_object_meta.interface_module)
                binder.install_class(factory_class(hana_object_meta.impl_class))
                binder.install_class(hana_object_meta.default_builder_class)

                binder.install_module(hana_binary_serializer_module(hana_object_meta.binary_serializer_class))
                binder.install_module(hana_readable_serializer_module(hana_object_meta.readable_serializer_class))
                binder.install_module(hana_binary_deserializer_module(hana_object_meta.binary_deserializer_class))
                binder.install_module(hana_readable_deserializer_module(hana_object_meta.readable_deserializer_class))

        return _HanaObjectModule


def hana_object_meta(cls) -> HanaObjectMeta:
    meta = hana_meta(cls)
    assert isinstance(meta, HanaObjectMeta)
    return meta
