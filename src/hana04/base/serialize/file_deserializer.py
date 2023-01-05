import json
from typing import Any

from hana04.base.serialize.readable.readable_deserializer import ReadableDeserializer
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import injectable_class, memoized


@memoized
@injectable_class
class FileDeserializer:
    def __init__(self, readable_deserializer_factory: ReadableDeserializer.Factory):
        self.readable_deserializer_factory = readable_deserializer_factory

    def readable_deserialize(self, file_name: str) -> Any:
        fin = open(file_name, "rt", encoding="utf-8")
        content = json.load(fin)
        deserializer = self.readable_deserializer_factory.create(file_name)
        return deserializer.deserialize(content)

    class Module(JyuusuModule):
        def configure(self, binder: Binder):
            binder.install_module(ReadableDeserializer.Module)
            binder.install_class(FileDeserializer)
