from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Dict, Any, Optional
from uuid import UUID, uuid4

from hana04.base.extension.hana_extensible import HanaExtensible
from hana04.base.serialize.binary.constants import TYPE_TAG, VALUE_TAG, UUID_TAG, EXTENSION_TAG
from hana04.base.type_ids import TYPE_ID_LOOKUP
from jyuusu.constructor_resolver import injectable_class, memoized

from jyuusu.binder import Module as JyuusuModule, Binder

T = TypeVar('T')


class TypeBinaryDeserializer(Generic[T], ABC):
    @abstractmethod
    def deserialize(self, value: Any, binary_deserializer: 'BinaryDeserializer') -> T:
        pass

    @abstractmethod
    def get_serialized_type(self) -> type:
        pass


@memoized
@injectable_class
class TypeIdToBinaryDeserializerMap:
    def __init__(self, type_id_to_deserializer_map: Dict[int, TypeBinaryDeserializer]):
        self.value = type_id_to_deserializer_map


class BinaryDeserializer:
    def __init__(self, file_name: Optional[str], type_id_to_deserializer_map: Dict[int, TypeBinaryDeserializer]):
        self.type_id_to_deserializer_map = type_id_to_deserializer_map
        self.file_name = file_name
        self.uuid_to_obj: Dict[UUID, Any] = {}

    def deserialize(self, dict_value: Dict[int, Any]):
        from hana04.base.serialize.hana_serializable import HanaSerializable

        assert TYPE_TAG in dict_value
        assert isinstance(dict_value[TYPE_TAG], int)
        assert VALUE_TAG in dict_value

        type_id = dict_value[TYPE_TAG]
        if type_id == TYPE_ID_LOOKUP:
            uuid = UUID(bytes=dict_value[VALUE_TAG])
            return self.uuid_to_obj[uuid]

        deserializer = self.type_id_to_deserializer_map[type_id]
        result = deserializer.deserialize(dict_value[VALUE_TAG], self)

        if isinstance(result, HanaSerializable):
            if UUID_TAG in dict_value:
                uuid = UUID(bytes=dict_value[UUID_TAG])
            else:
                uuid = uuid4()
            self.uuid_to_obj[uuid] = result

        return result

    def deserialize_extensions(self, dict_value: Dict[int, Any], hana_extensible: HanaExtensible):
        from hana04.base.serialize.hana_late_deserializable import HanaLateDeserializable

        if EXTENSION_TAG not in dict_value:
            return

        extension_values = dict_value[EXTENSION_TAG]
        assert isinstance(extension_values, list)

        for extension_value in extension_values:
            assert isinstance(extension_value, dict)
            assert TYPE_TAG in extension_value
            type_id = extension_value[TYPE_TAG]
            assert isinstance(type_id, int)
            assert type_id in self.type_id_to_deserializer_map
            deserializer = self.type_id_to_deserializer_map[type_id]
            deserialized_type = deserializer.get_serialized_type()
            assert issubclass(deserialized_type, HanaLateDeserializable)
            extension = hana_extensible.get_extension(deserialized_type)
            assert isinstance(extension, HanaLateDeserializable)
            extension.binary_deserialize(extension_value, self)

    @injectable_class
    class Factory:
        def __init__(self, type_id_to_deserializer_map: TypeIdToBinaryDeserializerMap):
            self.type_id_to_deserializer_map = type_id_to_deserializer_map.value

        def create(self, file_name: Optional[str] = None):
            return BinaryDeserializer(file_name, self.type_id_to_deserializer_map)

    class Module(JyuusuModule):
        def configure(self, binder: Binder):
            binder.install_dict(int, TypeBinaryDeserializer)
            binder.install_class(TypeIdToBinaryDeserializerMap)
            binder.install_class(BinaryDeserializer.Factory)
