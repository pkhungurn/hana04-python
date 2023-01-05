import unittest
from io import BytesIO
from typing import Optional, List, Dict
from unittest import TestCase, TestSuite

import msgpack
import numpy

from hana04.apt.extensible.hana_meta import hana_module
from hana04.apt.extensible.hana_object_decorators import hana_object, hana_property
from hana04.apt.extensible.hana_object_meta import HanaObjectMeta
from hana04.base.caching.cache_key import CacheKey
from hana04.base.caching.wrapped import Wrapped, Cached, Direct
from hana04.base.changeprop.variable import Variable
from hana04.base.extension.hana_object import HanaObject
from hana04.base.module import HanaBaseModule
from hana04.base.serialize.binary.binary_deserializer import BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import BinarySerializer
from hana04.base.serialize.binary.constants import EXTENSION_TAG, TYPE_TAG, VALUE_TAG, UUID_TAG
from hana04.base.serialize.readable.readable_deserializer import ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import ReadableSerializer
from hana04.base.type_ids import TYPE_ID_HANA_MAP_ENTRY
from hana04.base.util.message_packer import MessagePacker
from hana04.serialize.module import HanaSerializeModule
from hana04.serialize.type_ids import TYPE_ID_INTEGER, TYPE_ID_LONG, TYPE_ID_DIRECT, TYPE_ID_STRING
from jyuusu.factory_resolver import factory_class
from jyuusu.injectors import create_injector


@hana_object
class Aaa(HanaObject):
    _HANA_META = HanaObjectMeta(
        type_id=-10010,
        type_names=["base.decorators.Aaa"])

    @hana_property(_HANA_META, 1)
    def intField(self) -> numpy.int32:
        pass

    @hana_property(_HANA_META, 2)
    def longField(self) -> numpy.int64:
        pass

    @hana_property(_HANA_META, 3)
    def optionalIntField(self) -> Optional[numpy.int32]:
        pass

    @hana_property(_HANA_META, 4)
    def wrappedIntField(self) -> Wrapped[numpy.int32]:
        pass

    @hana_property(_HANA_META, 5)
    def intListField(self) -> List[numpy.int32]:
        pass

    @hana_property(_HANA_META, 6)
    def stringIntMapField(self) -> Dict[str, numpy.int32]:
        pass

    @hana_property(_HANA_META, 7)
    def varIntField(self) -> Variable[numpy.int32]:
        pass


class HanaObjectSerializationTest(TestCase):
    def setUp(self) -> None:
        self.injector = create_injector(
            HanaBaseModule,
            HanaSerializeModule,
            hana_module(Aaa))

    def create_AAA_raw_data(self):
        raw_data = Aaa._HANA_META.raw_data_class()
        raw_data.intField = numpy.int32(10)
        raw_data.longField = numpy.int64(20)
        raw_data.optionalIntField = numpy.int32(30)
        raw_data.wrappedIntField = Cached.of(CacheKey.Builder("123").add_string_part("abc").build())
        raw_data.intListField = [numpy.int32(1), numpy.int32(2), numpy.int32(3)]
        raw_data.stringIntMapField = {
            "a": numpy.int32(1),
            "b": numpy.int32(2),
        }
        raw_data.varIntField = numpy.int32(40)
        return raw_data

    def test_hana_object_get_readable_children_list(self):
        factory = self.injector.get_instance(factory_class(Aaa._HANA_META.impl_class))
        raw_data = self.create_AAA_raw_data()
        instance = factory.create(raw_data)
        readable_serializer = self.injector.get_instance(ReadableSerializer.Factory).create()

        children_list = instance.get_readable_children_list(readable_serializer)

        self.assertEqual(
            children_list,
            [
                {"func": "intField", "type": "Integer", "value": 10},
                {"func": "longField", "type": "Long", "value": 20},
                {"func": "optionalIntField", "type": "Integer", "value": 30},
                {
                    "func": "wrappedIntField",
                    "type": "Cached",
                    "value": {
                        "type": "CacheKey",
                        "protocol": "123",
                        "parts": ["abc"]
                    }
                },
                {"func": "intListField", "type": "Integer", "value": 1},
                {"func": "intListField", "type": "Integer", "value": 2},
                {"func": "intListField", "type": "Integer", "value": 3},
                {
                    "func": "stringIntMapField",
                    "type": "HanaMapEntry",
                    "key": {"type": "String", "value": "a"},
                    "value": {"type": "Integer", "value": 1}
                },
                {
                    "func": "stringIntMapField",
                    "type": "HanaMapEntry",
                    "key": {"type": "String", "value": "b"},
                    "value": {"type": "Integer", "value": 2}
                },
                {"func": "varIntField", "type": "Integer", "value": 40},
            ]
        )

    def test_hana_object_binary_serialize_content(self):
        factory = self.injector.get_instance(factory_class(Aaa._HANA_META.impl_class))
        raw_data = self.create_AAA_raw_data()
        raw_data.optionalIntField = None
        raw_data.wrappedIntField = Direct.of(numpy.int32(1))
        instance: Aaa = factory.create(raw_data)

        buffer = BytesIO()
        packer = MessagePacker(buffer)
        serializer_factory: BinarySerializer.Factory = self.injector.get_instance(BinarySerializer.Factory)
        serializer = serializer_factory.create(packer)

        instance.binary_serialize_content(packer, serializer)

        serialized = msgpack.unpackb(buffer.getvalue(), strict_map_key=False)
        self.assertEqual(serialized, {
            EXTENSION_TAG: [],
            1: {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 10},
            2: {TYPE_TAG: TYPE_ID_LONG, VALUE_TAG: 20},
            4: {TYPE_TAG: TYPE_ID_DIRECT, VALUE_TAG: {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 1}},
            5: [
                {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 1},
                {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 2},
                {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 3},
            ],
            6: [
                {
                    TYPE_TAG: TYPE_ID_HANA_MAP_ENTRY,
                    VALUE_TAG: [{TYPE_TAG: TYPE_ID_STRING, VALUE_TAG: "a"}, {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 1}]
                },
                {
                    TYPE_TAG: TYPE_ID_HANA_MAP_ENTRY,
                    VALUE_TAG: [{TYPE_TAG: TYPE_ID_STRING, VALUE_TAG: "b"}, {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 2}]
                },
            ],
            7: {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 40}
        })

    def test_readable_deserialization(self):
        deserializer: ReadableDeserializer = self.injector.get_instance(ReadableDeserializer.Factory).create()

        deserialized = deserializer.deserialize({
            "type": "base.decorators.Aaa",
            "children": [
                {"func": "intField", "type": "Integer", "value": 10},
                {"func": "longField", "type": "Long", "value": 20},
                {"func": "optionalIntField", "type": "Integer", "value": 30},
                {
                    "func": "wrappedIntField",
                    "type": "Cached",
                    "value": {
                        "type": "CacheKey",
                        "protocol": "123",
                        "parts": ["abc"]
                    }
                },
                {"func": "intListField", "type": "Integer", "value": 1},
                {"func": "intListField", "type": "Integer", "value": 2},
                {"func": "intListField", "type": "Integer", "value": 3},
                {
                    "func": "stringIntMapField",
                    "type": "HanaMapEntry",
                    "key": {"type": "String", "value": "a"},
                    "value": {"type": "Integer", "value": 1}
                },
                {
                    "func": "stringIntMapField",
                    "type": "HanaMapEntry",
                    "key": {"type": "String", "value": "b"},
                    "value": {"type": "Integer", "value": 2}
                },
                {"func": "varIntField", "type": "Integer", "value": 40},
            ]
        })

        self.assertTrue(isinstance(deserialized, Aaa))
        self.assertEqual(deserialized.intField(), numpy.int32(10))
        self.assertEqual(deserialized.longField(), numpy.int64(20))
        self.assertEqual(deserialized.optionalIntField(), numpy.int32(30))
        self.assertEqual(deserialized.wrappedIntField(),
                         Cached.of(CacheKey.Builder("123").add_string_part("abc").build()))
        self.assertEqual(deserialized.intListField(), [numpy.int32(1), numpy.int32(2), numpy.int32(3)])
        self.assertEqual(deserialized.stringIntMapField(),
                         {"a": numpy.int32(1), "b": numpy.int32(2)})
        self.assertEqual(deserialized.varIntField().value(), numpy.int32(40))

    def test_binary_deserialization(self):
        deserializer: BinaryDeserializer = self.injector.get_instance(BinaryDeserializer.Factory).create()

        deserialized = deserializer.deserialize({
            TYPE_TAG: -10010,
            VALUE_TAG: {
                EXTENSION_TAG: [],
                1: {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 10},
                2: {TYPE_TAG: TYPE_ID_LONG, VALUE_TAG: 20},
                4: {TYPE_TAG: TYPE_ID_DIRECT, VALUE_TAG: {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 1}},
                5: [
                    {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 1},
                    {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 2},
                    {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 3},
                ],
                6: [
                    {
                        TYPE_TAG: TYPE_ID_HANA_MAP_ENTRY,
                        VALUE_TAG: [{TYPE_TAG: TYPE_ID_STRING, VALUE_TAG: "a"},
                                    {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 1}]
                    },
                    {
                        TYPE_TAG: TYPE_ID_HANA_MAP_ENTRY,
                        VALUE_TAG: [{TYPE_TAG: TYPE_ID_STRING, VALUE_TAG: "b"},
                                    {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 2}]
                    },
                ],
                7: {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 40}
            },
        })

        self.assertTrue(isinstance(deserialized, Aaa))
        self.assertEqual(deserialized.intField(), numpy.int32(10))
        self.assertEqual(deserialized.longField(), numpy.int64(20))
        self.assertEqual(deserialized.optionalIntField(), None)
        self.assertEqual(deserialized.wrappedIntField().value, numpy.int32(1))
        self.assertEqual(deserialized.intListField(), [numpy.int32(1), numpy.int32(2), numpy.int32(3)])
        self.assertEqual(deserialized.stringIntMapField(),
                         {"a": numpy.int32(1), "b": numpy.int32(2)})
        self.assertEqual(deserialized.varIntField().value(), numpy.int32(40))

    def test_readable_serialization(self):
        factory = self.injector.get_instance(factory_class(Aaa._HANA_META.impl_class))
        raw_data = self.create_AAA_raw_data()
        instance = factory.create(raw_data)
        readable_serializer: ReadableSerializer = self.injector.get_instance(ReadableSerializer.Factory).create()

        serialized = readable_serializer.serialize(instance)

        self.assertEqual(serialized["type"], "base.decorators.Aaa")
        self.assertEqual(serialized["extensions"], [])
        self.assertTrue("id" in serialized)
        self.assertEqual(
            serialized["children"],
            [
                {"func": "intField", "type": "Integer", "value": 10},
                {"func": "longField", "type": "Long", "value": 20},
                {"func": "optionalIntField", "type": "Integer", "value": 30},
                {
                    "func": "wrappedIntField",
                    "type": "Cached",
                    "value": {
                        "type": "CacheKey",
                        "protocol": "123",
                        "parts": ["abc"]
                    }
                },
                {"func": "intListField", "type": "Integer", "value": 1},
                {"func": "intListField", "type": "Integer", "value": 2},
                {"func": "intListField", "type": "Integer", "value": 3},
                {
                    "func": "stringIntMapField",
                    "type": "HanaMapEntry",
                    "key": {"type": "String", "value": "a"},
                    "value": {"type": "Integer", "value": 1}
                },
                {
                    "func": "stringIntMapField",
                    "type": "HanaMapEntry",
                    "key": {"type": "String", "value": "b"},
                    "value": {"type": "Integer", "value": 2}
                },
                {"func": "varIntField", "type": "Integer", "value": 40},
            ])

    def test_binary_serialization(self):
        factory = self.injector.get_instance(factory_class(Aaa._HANA_META.impl_class))
        raw_data = self.create_AAA_raw_data()
        raw_data.optionalIntField = None
        raw_data.wrappedIntField = Direct.of(numpy.int32(1))
        instance: Aaa = factory.create(raw_data)

        buffer = BytesIO()
        packer = MessagePacker(buffer)
        serializer_factory: BinarySerializer.Factory = self.injector.get_instance(BinarySerializer.Factory)
        serializer = serializer_factory.create(packer)

        serializer.serialize(instance)

        serialized = msgpack.unpackb(buffer.getvalue(), strict_map_key=False)
        self.assertTrue(serialized[TYPE_TAG], -10010)
        self.assertTrue(UUID_TAG in serialized)
        self.assertTrue(isinstance(serialized[UUID_TAG], bytes))
        self.assertTrue(
            serialized[VALUE_TAG],
            {
                EXTENSION_TAG: [],
                1: {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 10},
                2: {TYPE_TAG: TYPE_ID_LONG, VALUE_TAG: 20},
                4: {TYPE_TAG: TYPE_ID_DIRECT, VALUE_TAG: {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 1}},
                5: [
                    {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 1},
                    {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 2},
                    {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 3},
                ],
                6: [
                    {
                        TYPE_TAG: TYPE_ID_HANA_MAP_ENTRY,
                        VALUE_TAG: [{TYPE_TAG: TYPE_ID_STRING, VALUE_TAG: "a"},
                                    {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 1}]
                    },
                    {
                        TYPE_TAG: TYPE_ID_HANA_MAP_ENTRY,
                        VALUE_TAG: [{TYPE_TAG: TYPE_ID_STRING, VALUE_TAG: "b"},
                                    {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 2}]
                    },
                ],
                7: {TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 40}
            })


def define_test_suite(suite: TestSuite):
    suite.addTest(unittest.makeSuite(HanaObjectSerializationTest))


if __name__ == "__main__":
    unittest.main()
