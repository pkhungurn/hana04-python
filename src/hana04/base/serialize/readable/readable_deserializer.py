from abc import ABC, abstractmethod
from typing import Optional, Dict, TypeVar, Generic, Any

from hana04.base.extension.hana_extensible import HanaExtensible
from hana04.base.serialize.readable.constants import LOOK_UP_TYPE_NAME
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import injectable_class, memoized

T = TypeVar('T')


class TypeReadableDeserializer(Generic[T], ABC):
    @abstractmethod
    def deserialize(self, json: Dict[str, Any], deserializer: 'ReadableDeserializer'):
        pass

    @abstractmethod
    def get_serialized_type(self) -> type:
        pass


@memoized
@injectable_class
class TypeNameToReadiableDeserializerMap:
    def __init__(self, value: Dict[str, TypeReadableDeserializer]):
        self.value = value


class ReadableDeserializer:
    def __init__(self,
                 file_name: Optional[str],
                 type_name_to_deserializer: Dict[str, TypeReadableDeserializer]):
        from hana04.base.serialize.hana_serializable import HanaSerializable
        self.file_name = file_name
        self.type_name_to_deserializer = type_name_to_deserializer
        self.uuid_to_obj: Dict[str, HanaSerializable] = {}

    def deserialize(self, json: Dict[str, Any]) -> Any:
        from hana04.base.serialize.hana_serializable import HanaSerializable

        assert "type" in json and json["type"] is not None
        type_name = json["type"]

        if type_name == LOOK_UP_TYPE_NAME:
            assert "id" in json and isinstance(json["id"], str)
            return self.uuid_to_obj[json["id"]]

        deserializer = self.type_name_to_deserializer[type_name]
        result = deserializer.deserialize(json, self)
        if isinstance(result, HanaSerializable) and "id" in json:
            assert isinstance(json["id"], str)
            self.uuid_to_obj[json["id"]] = result
        return result

    def deserialize_extensions(self, json: Dict[str, Any], hana_extensible: HanaExtensible):
        from hana04.base.serialize.hana_late_deserializable import HanaLateDeserializable

        if "extensions" not in json:
            return
        extension_jsons = json["extensions"]
        assert isinstance(extension_jsons, list)

        for extension_json in extension_jsons:
            assert isinstance(extension_json, dict)
            assert "type" in extension_json
            type_name = extension_json["type"]
            assert isinstance(type_name, str)
            assert type_name in self.type_name_to_deserializer
            deserializer = self.type_name_to_deserializer[type_name]
            deserialized_type = deserializer.get_serialized_type()
            assert issubclass(deserialized_type, HanaLateDeserializable)
            extension = hana_extensible.get_extension(deserialized_type)
            assert isinstance(extension, HanaLateDeserializable)
            extension.readable_deserialize(extension_json, self)

    @injectable_class
    class Factory:
        def __init__(self, type_name_to_readable_deserializer: TypeNameToReadiableDeserializerMap):
            self.type_name_to_readable_deserializer = type_name_to_readable_deserializer.value

        def create(self, file_name: Optional[str] = None):
            return ReadableDeserializer(file_name, self.type_name_to_readable_deserializer)

    class Module(JyuusuModule):
        def configure(self, binder: Binder):
            binder.install_dict(str, TypeReadableDeserializer)
            binder.install_class(TypeNameToReadiableDeserializerMap)
            binder.install_class(ReadableDeserializer.Factory)
