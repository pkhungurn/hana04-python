from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, Generic, TypeVar, List
from uuid import UUID, uuid4

from hana04.base.extension.hana_extensible import HanaExtensible
from hana04.base.serialize.readable.constants import LOOK_UP_TYPE_NAME
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import injectable_class, memoized

T = TypeVar('T')


class TypeReadableSerializer(Generic[T], ABC):
    @abstractmethod
    def serialize(self, obj: T, serializer: 'ReadableSerializer') -> Dict[str, Any]:
        pass


@memoized
@injectable_class
class TypeNameToReadableSerializerMap:
    def __init__(self, value: Dict[str, TypeReadableSerializer]):
        self.value = value


@memoized
@injectable_class
class TypeToReadableSerializerMap:
    def __init__(self, value: Dict[type, TypeReadableSerializer]):
        self.value = value


class ReadableSerializer:
    def __init__(self,
                 file_name: Optional[str],
                 type_name_to_serializer: Dict[str, TypeReadableSerializer],
                 type_to_serializer: Dict[type, TypeReadableSerializer]):
        self.type_to_serializer = type_to_serializer
        self.type_name_to_serializer = type_name_to_serializer
        self.file_name = file_name
        self.obj_id_to_uuid: Dict[int, UUID] = {}

    def add_func(self, json: Dict[str, Any], func: Optional[str]):
        if func is None:
            return json
        else:
            json["func"] = func
            return json

    def serialize(self, obj: Any, func: Optional[str] = None) -> Dict[str, Any]:
        from hana04.base.serialize.hana_serializable import HanaSerializable

        if id(obj) in self.obj_id_to_uuid:
            return self.add_func(
                {
                    "type": LOOK_UP_TYPE_NAME,
                    "id": str(self.obj_id_to_uuid[id(obj)])
                },
                func)

        if isinstance(obj, HanaSerializable):
            serializer = self.type_name_to_serializer[obj.get_serialized_type_name()]
        else:
            serializer = self.type_to_serializer[obj.__class__]
        result = serializer.serialize(obj, self)

        if isinstance(obj, HanaSerializable):
            uuid = uuid4()
            self.obj_id_to_uuid[id(obj)] = uuid
            result["id"] = str(uuid)

        return self.add_func(result, func)

    def serialize_extensions(self, hana_extensible: HanaExtensible) -> List[Dict[str, Any]]:
        from hana04.base.serialize.hana_late_deserializable import HanaLateDeserializable

        result = []
        for extension in hana_extensible.get_extensions():
            if isinstance(extension, HanaLateDeserializable):
                result.append(self.serialize(extension))
        return result

    @injectable_class
    class Factory:
        def __init__(self,
                     type_name_to_serializer: TypeNameToReadableSerializerMap,
                     type_to_serializer: TypeToReadableSerializerMap):
            self.type_to_serializer = type_to_serializer.value
            self.type_name_to_serializer = type_name_to_serializer.value

        def create(self, file_name: Optional[str] = None):
            return ReadableSerializer(file_name, self.type_name_to_serializer, self.type_to_serializer)

    class Module(JyuusuModule):
        def configure(self, binder: Binder):
            binder.install_dict(str, TypeReadableSerializer)
            binder.install_class(TypeNameToReadableSerializerMap)
            binder.install_dict(type, TypeReadableSerializer)
            binder.install_class(TypeToReadableSerializerMap)
            binder.install_class(ReadableSerializer.Factory)
