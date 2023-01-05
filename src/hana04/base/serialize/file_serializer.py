import json
import os
from typing import Any

from hana04.base.serialize.readable.readable_serializer import ReadableSerializer
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import injectable_class, memoized


@memoized
@injectable_class
class FileSerializer:
    def __init__(self, readable_serializer_factory: ReadableSerializer.Factory):
        self.readable_serializer_factory = readable_serializer_factory

    def readable_serialize(self, obj: Any, file_name: str):
        content = self.readable_serializer_factory.create(file_name).serialize(obj)
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, "wt", encoding='utf-8') as fout:
            fout.write(json.dumps(content, indent=2, ensure_ascii=False))

    class Module(JyuusuModule):
        def configure(self, binder: Binder):
            binder.install_module(ReadableSerializer.Module)
            binder.install_class(FileSerializer)