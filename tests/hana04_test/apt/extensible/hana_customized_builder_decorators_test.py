import unittest
from unittest import TestSuite

from hana04.base.module import HanaBaseModule
from hana04.serialize.module import HanaSerializeModule
from hana04.apt.extensible.hana_customized_builder_decorators import hana_customized_builder, \
    hana_customized_builder_module
from hana04.apt.extensible.hana_meta import hana_module
from hana04.apt.extensible.hana_object_decorators import hana_property, hana_object
from hana04.apt.extensible.hana_object_meta import HanaObjectMeta, hana_object_meta
from hana04.base.extension.hana_object import HanaObject
from hana04.base.serialize.binary.binary_deserializer import BinaryDeserializer
from hana04.base.serialize.binary.constants import TYPE_TAG, VALUE_TAG
from hana04.base.serialize.readable.readable_deserializer import ReadableDeserializer
from jyuusu.constructor_resolver import injectable_class
from jyuusu.injectors import create_injector


@hana_object
class Aaa(HanaObject):
    _HANA_META = HanaObjectMeta(
        type_id=-10010,
        type_names=["Aaa"])

    @hana_property(_HANA_META, 1)
    def stringField(self) -> str:
        pass


@hana_customized_builder(Aaa)
@injectable_class
class AaaBuilder(hana_object_meta(Aaa).default_builder_class):
    def __init__(self, impl_factory: hana_object_meta(Aaa).impl_factory_class):
        super().__init__(impl_factory)
        self.setStringField("default-value")


class HanaCustomizedBuilderDecoratorsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.injector = create_injector(
            HanaBaseModule,
            HanaSerializeModule,
            hana_module(Aaa),
            hana_customized_builder_module(AaaBuilder))

    def test_building_with_default_value(self):
        builder: AaaBuilder = self.injector.get_instance(AaaBuilder)

        created = builder.build()

        self.assertEqual(created.stringField(), "default-value")

    def test_readable_deserialization(self):
        deserializer: ReadableDeserializer = self.injector.get_instance(ReadableDeserializer.Factory).create()

        aaa = deserializer.deserialize({
            "type": "Aaa"
        })

        self.assertEqual(aaa.stringField(), "default-value")

    def test_binary_deserializer(self):
        deserializer: BinaryDeserializer = self.injector.get_instance(BinaryDeserializer.Factory).create()

        aaa = deserializer.deserialize({
            TYPE_TAG: -10010,
            VALUE_TAG: {}
        })

        self.assertEqual(aaa.stringField(), "default-value")


def define_test_suite(suite: TestSuite):
    suite.addTest(unittest.makeSuite(HanaCustomizedBuilderDecoratorsTest))


if __name__ == "__main__":
    unittest.main()
