from typing import List, Dict, Any

from hana04.apt.extensible.constants import HANA_META_PROPERTY_NAME
from hana04.apt.extensible.hana_object_meta import HanaObjectMeta
from hana04.apt.extensible.hana_property_spec import HanaPropertySpec
from hana04.apt.extensible.property_type_spec import VariableTypeSpec
from hana04.base.changeprop.variable import Variable
from hana04.base.extension.extensions.validator import Validator
from hana04.base.extension.hana_extensible import HanaExtensible
from hana04.base.serialize.binary.binary_deserializer import BinaryDeserializer
from hana04.base.serialize.binary.constants import VALUE_TAG
from hana04.base.serialize.hana_late_deserializable import HanaLateDeserializable
from hana04.base.serialize.readable.readable_deserializer import ReadableDeserializer
from jyuusu.factory_resolver import injectable_factory


class HanaLateDeserializableMeta(HanaObjectMeta):
    def __init__(self, type_id: int, type_names: List[str]):
        super().__init__(type_id, type_names)

    @staticmethod
    def assert_hana_late_deserializable_can_be_created(cls: type):
        HanaObjectMeta.assert_hana_object_can_be_created(cls)
        assert isinstance(cls.__dict__[HANA_META_PROPERTY_NAME], HanaLateDeserializableMeta)
        assert issubclass(cls, HanaLateDeserializable)

    def add_property(self, new_property: HanaPropertySpec):
        assert new_property.id not in self._property_by_id
        assert new_property.name not in self._property_by_name
        assert isinstance(new_property.type_spec, VariableTypeSpec)
        self._properties.append(new_property)
        self._property_by_id[new_property.id] = new_property
        self._property_by_name[new_property.name] = new_property

    def make_hana_late_deserializable(self, cls):
        self.make_hana_object(cls)

    def create_hana_late_deserializable_member_dict(self, cls):
        hana_meta = self

        def readable_deserialize(self, json: Dict[str, Any], deserializer: ReadableDeserializer):
            raw_data = hana_meta.raw_data_class()
            for child in HanaObjectMeta.valid_json_children(json, hana_meta):
                property_ = hana_meta._property_by_name[child["func"]]
                property_.readable_deserialize_into_raw_data(child, raw_data, deserializer)
            for property_ in hana_meta.properties:
                assert isinstance(property_.type_spec, VariableTypeSpec)
                variable = getattr(self, property_.private_field_name)
                assert isinstance(variable, Variable)
                variable.set(getattr(raw_data, property_.name))
            if isinstance(self, HanaExtensible):
                deserializer.deserialize_extensions(json, self)
            if self.supports_extension(Validator):
                validator: Validator = self.get_extension(Validator)
                validator.validate()

        def binary_deserialize(self, value: Dict[int, Any], deserializer: BinaryDeserializer):
            raw_data = hana_meta.raw_data_class()
            if VALUE_TAG in value:
                assert isinstance(value[VALUE_TAG], dict)
                for key_, value_ in value[VALUE_TAG].items():
                    assert isinstance(key_, int)
                    if key_ not in hana_meta._property_by_id:
                        continue
                    property_spec = hana_meta._property_by_id[key_]
                    property_spec.binary_deserialize_into_raw_data(value_, raw_data, deserializer)
                for property_ in hana_meta.properties:
                    assert isinstance(property_.type_spec, VariableTypeSpec)
                    variable = getattr(self, property_.private_field_name)
                    assert isinstance(variable, Variable)
                    variable.set(getattr(raw_data, property_.name))
            if isinstance(self, HanaExtensible):
                deserializer.deserialize_extensions(value, self)
            if self.supports_extension(Validator):
                validator: Validator = self.get_extension(Validator)
                validator.validate()

        members = self.create_hana_object_member_dict(cls)
        members["readable_deserialize"] = readable_deserialize
        members["binary_deserialize"] = binary_deserialize
        return members

    def create_impl_class(self, cls):
        members = self.create_hana_late_deserializable_member_dict(cls)
        _Impl = type("_Impl", (cls,), members)
        _Impl = injectable_factory("extension_uber_factory")(_Impl)
        return _Impl
