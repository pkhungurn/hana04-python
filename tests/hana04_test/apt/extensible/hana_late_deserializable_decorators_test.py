import unittest
from typing import List, Dict
from unittest import TestSuite

from hana04.base.module import HanaBaseModule
from hana04.serialize.module import HanaSerializeModule
from hana04.apt.extensible.hana_customized_builder_decorators import hana_customized_builder, \
    hana_customized_builder_module
from hana04.apt.extensible.hana_late_deserializable_decorators import hana_late_deserializable
from hana04.apt.extensible.hana_late_deserializable_meta import HanaLateDeserializableMeta
from hana04.apt.extensible.hana_meta import hana_module
from hana04.apt.extensible.hana_object_decorators import hana_property
from hana04.apt.extensible.hana_object_meta import hana_object_meta
from hana04.base.caching.cache_key import CacheKey
from hana04.base.caching.wrapped import Wrapped, Cached
from hana04.base.changeprop.variable import Variable
from hana04.base.serialize.binary.binary_deserializer import BinaryDeserializer
from hana04.base.serialize.binary.constants import TYPE_TAG, VALUE_TAG
from hana04.base.serialize.hana_late_deserializable import HanaLateDeserializable
from hana04.base.serialize.readable.readable_deserializer import ReadableDeserializer
from hana04.base.type_ids import TYPE_ID_HANA_MAP_ENTRY
from hana04.serialize.type_ids import TYPE_ID_STRING, TYPE_ID_BOOLEAN
from jyuusu.injectors import create_injector


@hana_late_deserializable
class Aaa(HanaLateDeserializable):
    _HANA_META = HanaLateDeserializableMeta(
        type_id=-10010,
        type_names=["Aaa"])

    @hana_property(_HANA_META, 1)
    def stringField(self) -> Variable[str]:
        pass

    @hana_property(_HANA_META, 2)
    def stringWrappedField(self) -> Variable[Wrapped[str]]:
        pass

    @hana_property(_HANA_META, 3)
    def stringListField(self) -> Variable[List[str]]:
        pass

    @hana_property(_HANA_META, 4)
    def stringBooleanMapField(self) -> Variable[Dict[str, bool]]:
        pass


@hana_customized_builder(Aaa)
class AaaBuilder(hana_object_meta(Aaa).default_builder_class):
    def __init__(self, impl_factory: hana_object_meta(Aaa).impl_factory_class):
        super().__init__(impl_factory)
        self.setStringField("default-value")
        self.setStringWrappedField("wrapped-default-value")
        self.addStringListField("a").addStringListField("b").addStringListField("c")
        self.putStringBooleanMapField("1", True).putStringBooleanMapField("2", False)


class HanaLateDeserializableDecoratorsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.injector = create_injector(
            HanaBaseModule,
            HanaSerializeModule,
            hana_module(Aaa),
            hana_customized_builder_module(AaaBuilder))

    def test_construction(self):
        builder: AaaBuilder = self.injector.get_instance(AaaBuilder)

        aaa = builder.build()

        self.assertEqual(aaa.stringField().value(), "default-value")
        self.assertEqual(aaa.stringWrappedField().value().value, "wrapped-default-value")
        self.assertEqual(aaa.stringListField().value(), ["a", "b", "c"])
        self.assertEqual(aaa.stringBooleanMapField().value(), {"1": True, "2": False})

    def test_readable_deserialize(self):
        aaa: Aaa = self.injector.get_instance(AaaBuilder).build()
        deserializer: ReadableDeserializer = self.injector.get_instance(ReadableDeserializer.Factory).create()

        aaa.readable_deserialize(
            {
                "type": "Aaa",
                "children": [
                    {
                        "func": "stringField",
                        "type": "String",
                        "value": "abc"
                    },
                    {
                        "func": "stringWrappedField",
                        "type": "Cached",
                        "value": {
                            "type": "CacheKey",
                            "protocol": "123",
                            "parts": ["abc"]
                        }
                    },
                    {
                        "func": "stringListField",
                        "type": "String",
                        "value": "111"
                    },
                    {
                        "func": "stringListField",
                        "type": "String",
                        "value": "222"
                    },
                    {
                        "func": "stringListField",
                        "type": "String",
                        "value": "333"
                    },
                    {
                        "func": "stringBooleanMapField",
                        "type": "HanaMapEntry",
                        "key": {"type": "String", "value": "key-1"},
                        "value": {"type": "Boolean", "value": True},
                    },
                    {
                        "func": "stringBooleanMapField",
                        "type": "HanaMapEntry",
                        "key": {"type": "String", "value": "key-2"},
                        "value": {"type": "Boolean", "value": False},
                    },
                ]
            },
            deserializer)

        self.assertEqual(aaa.stringField().value(), "abc")
        self.assertEqual(
            aaa.stringWrappedField().value(),
            Cached.of(CacheKey.Builder("123").add_string_part("abc").build()))
        self.assertEqual(aaa.stringListField().value(), ["111", "222", "333"])
        self.assertEqual(aaa.stringBooleanMapField().value(), {"key-1": True, "key-2": False})

    def test_binary_deserialize(self):
        aaa: Aaa = self.injector.get_instance(AaaBuilder).build()
        deserializer: BinaryDeserializer = self.injector.get_instance(BinaryDeserializer.Factory).create()

        aaa.binary_deserialize(
            {
                TYPE_TAG: -10010,
                VALUE_TAG: {
                    1: {TYPE_TAG: TYPE_ID_STRING, VALUE_TAG: "abc"},
                    2: {TYPE_TAG: TYPE_ID_STRING, VALUE_TAG: "bcd"},
                    3: [
                        {TYPE_TAG: TYPE_ID_STRING, VALUE_TAG: "111"},
                        {TYPE_TAG: TYPE_ID_STRING, VALUE_TAG: "222"},
                        {TYPE_TAG: TYPE_ID_STRING, VALUE_TAG: "333"},
                    ],
                    4: [
                        {
                            TYPE_TAG: TYPE_ID_HANA_MAP_ENTRY,
                            VALUE_TAG: [
                                {TYPE_TAG: TYPE_ID_STRING, VALUE_TAG: "key-1"},
                                {TYPE_TAG: TYPE_ID_BOOLEAN, VALUE_TAG: True},
                            ]
                        },
                        {
                            TYPE_TAG: TYPE_ID_HANA_MAP_ENTRY,
                            VALUE_TAG: [
                                {TYPE_TAG: TYPE_ID_STRING, VALUE_TAG: "key-2"},
                                {TYPE_TAG: TYPE_ID_BOOLEAN, VALUE_TAG: False},
                            ]
                        },
                    ]
                },
            },
            deserializer)

        self.assertEqual(aaa.stringField().value(), "abc")
        self.assertEqual(aaa.stringWrappedField().value().value, "bcd")
        self.assertEqual(aaa.stringListField().value(), ["111", "222", "333"])
        self.assertEqual(aaa.stringBooleanMapField().value(), {"key-1": True, "key-2": False})


def define_test_suite(suite: TestSuite):
    suite.addTest(unittest.makeSuite(HanaLateDeserializableDecoratorsTest))


if __name__ == "__main__":
    unittest.main()
