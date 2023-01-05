from jyuusu.binder import Binder, Module as JyuusuModule

import hana04.serialize.primitive.int32
import hana04.serialize.primitive.int64
import hana04.serialize.primitive.float32
import hana04.serialize.primitive.float64
import hana04.serialize.primitive.boolean
import hana04.serialize.primitive.string
import hana04.serialize.primitive.uuid_
import hana04.serialize.primitive.file_path
import hana04.serialize.primitive.cache_key
import hana04.serialize.primitive.direct
import hana04.serialize.primitive.cached


class HanaSerializeModule(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana04.serialize.primitive.int32.Module)
        binder.install_module(hana04.serialize.primitive.int64.Module)
        binder.install_module(hana04.serialize.primitive.float32.Module)
        binder.install_module(hana04.serialize.primitive.float64.Module)
        binder.install_module(hana04.serialize.primitive.boolean.Module)
        binder.install_module(hana04.serialize.primitive.string.Module)
        binder.install_module(hana04.serialize.primitive.uuid_.Module)
        binder.install_module(hana04.serialize.primitive.file_path.Module)
        binder.install_module(hana04.serialize.primitive.cache_key.Module)
        binder.install_module(hana04.serialize.primitive.direct.Module)
        binder.install_module(hana04.serialize.primitive.cached.Module)
