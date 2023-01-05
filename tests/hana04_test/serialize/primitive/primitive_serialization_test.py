import math
import unittest
from io import BytesIO
from typing import Optional
from unittest import TestCase, TestSuite
from uuid import UUID

import msgpack
import numpy

from hana04.base.caching.cache_key import CacheKey
from hana04.base.caching.wrapped import Direct, Cached
from hana04.base.filesystem.file_path import FilePath
from hana04.base.serialize.binary.binary_deserializer import BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import BinarySerializer
from hana04.base.serialize.binary.constants import TYPE_TAG, VALUE_TAG
from hana04.base.serialize.readable.readable_deserializer import ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import ReadableSerializer
from hana04.base.type_ids import TYPE_ID_HANA_MAP_ENTRY
from hana04.base.util.hana_map_entry import HanaMapEntry
from hana04.base.util.message_packer import MessagePacker
from hana04.serialize.type_ids import TYPE_ID_INTEGER, TYPE_ID_STRING, TYPE_ID_BOOLEAN, TYPE_ID_FILE_PATH, \
    TYPE_ID_CACHE_KEY, TYPE_ID_CACHED
from jyuusu.injectors import create_injector

from hana04.base.module import HanaBaseModule
from hana04.serialize.module import HanaSerializeModule


class PrimitiveReadableSerializationTest(TestCase):
    def setUp(self):
        self.injector = create_injector(
            HanaBaseModule,
            HanaSerializeModule)

    def test_serialize_int32(self):
        factory: ReadableSerializer.Factory = self.injector.get_instance(ReadableSerializer.Factory)
        serializer = factory.create()

        serialized = serializer.serialize(numpy.int32(10), "intField")

        self.assertEqual(serialized, {
            "func": "intField",
            "type": "Integer",
            "value": 10
        })

    def test_deserialize_int32(self):
        factory: ReadableDeserializer.Factory = self.injector.get_instance(ReadableDeserializer.Factory)
        deserializer = factory.create()

        deserialized = deserializer.deserialize({"type": "Integer", "value": 20})

        self.assertEqual(deserialized, numpy.int32(20))

    def test_serialize_int64(self):
        factory: ReadableSerializer.Factory = self.injector.get_instance(ReadableSerializer.Factory)
        serializer = factory.create()

        serialized = serializer.serialize(numpy.int64(10000000000), "longField")

        self.assertEqual(serialized, {
            "func": "longField",
            "type": "Long",
            "value": 10000000000
        })

    def test_deserialize_int64(self):
        factory: ReadableDeserializer.Factory = self.injector.get_instance(ReadableDeserializer.Factory)
        deserializer = factory.create()

        deserialized = deserializer.deserialize({"type": "Long", "value": 100000000000})

        self.assertEqual(deserialized, numpy.int64(100000000000))

    def test_serialize_float32(self):
        factory: ReadableSerializer.Factory = self.injector.get_instance(ReadableSerializer.Factory)
        serializer = factory.create()

        serialized = serializer.serialize(numpy.float32(math.pi))

        self.assertEqual(serialized["type"], "Float")
        self.assertAlmostEqual(serialized["value"], math.pi, places=6)

    def test_deserialize_float32(self):
        factory: ReadableDeserializer.Factory = self.injector.get_instance(ReadableDeserializer.Factory)
        deserializer = factory.create()

        deserialized = deserializer.deserialize({"type": "Float", "value": 3.1415})

        self.assertEqual(deserialized, numpy.float32(3.1415))

    def test_serialize_float64(self):
        factory: ReadableSerializer.Factory = self.injector.get_instance(ReadableSerializer.Factory)
        serializer = factory.create()

        serialized = serializer.serialize(numpy.float64(math.pi))

        self.assertEqual(serialized["type"], "Double")
        self.assertAlmostEqual(serialized["value"], math.pi, places=12)

    def test_deserialize_float64(self):
        factory: ReadableDeserializer.Factory = self.injector.get_instance(ReadableDeserializer.Factory)
        deserializer = factory.create()

        deserialized = deserializer.deserialize({"type": "Double", "value": 3.1415})

        self.assertEqual(deserialized, numpy.float64(3.1415))

    def test_serialize_boolean(self):
        factory: ReadableSerializer.Factory = self.injector.get_instance(ReadableSerializer.Factory)
        serializer = factory.create()

        serialized = serializer.serialize(True)

        self.assertEqual(serialized, {"type": "Boolean", "value": True})

    def test_deserialize_boolean(self):
        factory: ReadableDeserializer.Factory = self.injector.get_instance(ReadableDeserializer.Factory)
        deserializer = factory.create()

        deserialized = deserializer.deserialize({"type": "Boolean", "value": False})

        self.assertEqual(deserialized, False)

    def test_serialize_string(self):
        factory: ReadableSerializer.Factory = self.injector.get_instance(ReadableSerializer.Factory)
        serializer = factory.create()

        serialized = serializer.serialize("abc")

        self.assertEqual(serialized, {"type": "String", "value": "abc"})

    def test_deserialize_string(self):
        factory: ReadableDeserializer.Factory = self.injector.get_instance(ReadableDeserializer.Factory)
        deserializer = factory.create()

        deserialized = deserializer.deserialize({"type": "String", "value": "abc"})

        self.assertEqual(deserialized, "abc")

    def test_serialize_uuid(self):
        factory: ReadableSerializer.Factory = self.injector.get_instance(ReadableSerializer.Factory)
        serializer = factory.create()

        serialized = serializer.serialize(UUID("123e4567-e89b-12d3-a456-426614174000"))

        self.assertEqual(serialized, {"type": "Uuid", "value": "123e4567-e89b-12d3-a456-426614174000"})

    def test_deserialize_uuid(self):
        factory: ReadableDeserializer.Factory = self.injector.get_instance(ReadableDeserializer.Factory)
        deserializer = factory.create()

        deserialized = deserializer.deserialize({"type": "Uuid", "value": "123e4567-e89b-12d3-a456-426614174000"})

        self.assertEqual(deserialized, UUID("123e4567-e89b-12d3-a456-426614174000"))

    def test_serialize_file_path_not_relative(self):
        factory: ReadableSerializer.Factory = self.injector.get_instance(ReadableSerializer.Factory)
        serializer = factory.create()

        serialized = serializer.serialize(FilePath(save_as_relative=False, stored_path="a/b/c/d.txt"))

        self.assertEqual(serialized, {"type": "FilePath", "relative": False, "value": "a/b/c/d.txt"})

    def test_deserialize_file_path_not_relative(self):
        factory: ReadableDeserializer.Factory = self.injector.get_instance(ReadableDeserializer.Factory)
        deserializer = factory.create()

        deserialized = deserializer.deserialize({"type": "FilePath", "relative": False, "value": "a/b/c/d.txt"})

        self.assertEqual(deserialized, FilePath(save_as_relative=False, stored_path="a/b/c/d.txt"))

    def test_serialize_file_path_relative(self):
        factory: ReadableSerializer.Factory = self.injector.get_instance(ReadableSerializer.Factory)
        serializer = factory.create("a/e/f.json")

        serialized = serializer.serialize(FilePath(save_as_relative=True, stored_path="a/b/c/d.txt"))

        self.assertEqual(serialized, {"type": "FilePath", "relative": True, "value": "../b/c/d.txt"})

    def test_deserialize_file_path_relative(self):
        factory: ReadableDeserializer.Factory = self.injector.get_instance(ReadableDeserializer.Factory)
        deserializer = factory.create("a/e/f.json")

        deserialized = deserializer.deserialize({"type": "FilePath", "relative": True, "value": "../b/c/d.txt"})

        self.assertEqual(deserialized, FilePath(save_as_relative=True, stored_path="a/b/c/d.txt"))

    def test_serialize_cache_key(self):
        factory: ReadableSerializer.Factory = self.injector.get_instance(ReadableSerializer.Factory)
        serializer = factory.create()

        serialized = serializer.serialize(
            CacheKey.Builder("123")
            .add_string_part("abc")
            .add_file_path_part(FilePath.absolute("a/b/c.txt"))
            .build())

        self.assertEqual(
            serialized,
            {
                "type": "CacheKey",
                "protocol": "123",
                "parts": [
                    "abc",
                    {
                        "type": "FilePath",
                        "relative": False,
                        "value": "a/b/c.txt"
                    }
                ]
            })

    def test_deserialize_cache_key(self):
        factory: ReadableDeserializer.Factory = self.injector.get_instance(ReadableDeserializer.Factory)
        deserializer = factory.create("a/e/f.json")

        deserialized = deserializer.deserialize({
            "type": "CacheKey",
            "protocol": "123",
            "parts": [
                "abc",
                {
                    "type": "FilePath",
                    "relative": True,
                    "value": "../../b.txt"
                }
            ]
        })

        self.assertEqual(
            deserialized,
            CacheKey.Builder("123")
            .add_string_part("abc")
            .add_file_path_part(FilePath.relative("b.txt"))
            .build())

    def test_serialize_direct(self):
        factory: ReadableSerializer.Factory = self.injector.get_instance(ReadableSerializer.Factory)
        serializer = factory.create()

        serialized = serializer.serialize(Direct.of(numpy.int32(10)))

        self.assertEqual(
            serialized,
            {
                "type": "Direct",
                "value": {"type": "Integer", "value": 10}
            })

    def test_deserialize_direct(self):
        factory: ReadableDeserializer.Factory = self.injector.get_instance(ReadableDeserializer.Factory)
        deserializer = factory.create()

        deserialized = deserializer.deserialize({
            "type": "Direct",
            "value": {"type": "Integer", "value": 10}
        })

        self.assertTrue(isinstance(deserialized, Direct))
        self.assertEqual(deserialized.value, numpy.int32(10))

    def test_serialize_cached(self):
        factory: ReadableSerializer.Factory = self.injector.get_instance(ReadableSerializer.Factory)
        serializer = factory.create()

        serialized = serializer.serialize(
            Cached.of(CacheKey.Builder("123").add_string_part("abc").build()))

        self.assertEqual(
            serialized,
            {
                "type": "Cached",
                "value": {"type": "CacheKey", "protocol": "123", "parts": ["abc"]}
            })

    def test_deserialize_cached(self):
        factory: ReadableDeserializer.Factory = self.injector.get_instance(ReadableDeserializer.Factory)
        deserializer = factory.create()

        deserialized = deserializer.deserialize({
            "type": "Cached",
            "value": {"type": "CacheKey", "protocol": "123", "parts": ["abc"]}
        })

        self.assertEqual(deserialized, Cached.of(CacheKey.Builder("123").add_string_part("abc").build()))

    def test_serialize_HanaMapEntry(self):
        factory: ReadableSerializer.Factory = self.injector.get_instance(ReadableSerializer.Factory)
        serializer = factory.create()

        serialized = serializer.serialize(HanaMapEntry("abc", numpy.int32(10)))

        self.assertEqual(
            serialized,
            {
                "type": "HanaMapEntry",
                "key": {"type": "String", "value": "abc"},
                "value": {"type": "Integer", "value": 10}
            })

    def test_deserialize_HanaMapEntry(self):
        factory: ReadableDeserializer.Factory = self.injector.get_instance(ReadableDeserializer.Factory)
        deserializer = factory.create()

        deserialized = deserializer.deserialize({
            "type": "HanaMapEntry",
            "key": {"type": "String", "value": "abc"},
            "value": {"type": "Integer", "value": 10}
        })

        self.assertEqual(deserialized, HanaMapEntry("abc", numpy.int32(10)))


class PrimitiveBinarySerializationTest(TestCase):
    def setUp(self):
        self.injector = create_injector(
            HanaBaseModule,
            HanaSerializeModule)

    def create_serializer_and_buffer(self, file_name: Optional[str] = None):
        buffer = BytesIO()
        packer = MessagePacker(buffer)
        factory: BinarySerializer.Factory = self.injector.get_instance(BinarySerializer.Factory)
        return factory.create(packer, file_name), buffer

    def create_deserializer(self, file_name: Optional[str] = None):
        factory: BinaryDeserializer.Factory = self.injector.get_instance(BinaryDeserializer.Factory)
        deserializer = factory.create(file_name)
        return deserializer

    def test_serialize_int32(self):
        serializer, buffer = self.create_serializer_and_buffer()

        serializer.serialize(numpy.int32(10))

        serialized = msgpack.unpackb(buffer.getvalue(), strict_map_key=False)
        self.assertEqual(
            serialized,
            {
                TYPE_TAG: TYPE_ID_INTEGER,
                VALUE_TAG: 10
            })

    def test_deserialize_int32(self):
        deserializer = self.create_deserializer()

        deserialized = deserializer.deserialize({TYPE_TAG: TYPE_ID_INTEGER, VALUE_TAG: 10})

        self.assertEqual(deserialized, numpy.int32(10))

    def test_serialize_bool(self):
        serializer, buffer = self.create_serializer_and_buffer()

        serializer.serialize(True)

        serialized = msgpack.unpackb(buffer.getvalue(), strict_map_key=False)
        self.assertEqual(
            serialized,
            {
                TYPE_TAG: TYPE_ID_BOOLEAN,
                VALUE_TAG: True
            })

    def test_deserialize_bool(self):
        deserializer = self.create_deserializer()

        deserialized = deserializer.deserialize({TYPE_TAG: TYPE_ID_BOOLEAN, VALUE_TAG: False})

        self.assertEqual(deserialized, False)

    def test_serialize_str(self):
        serializer, buffer = self.create_serializer_and_buffer()

        serializer.serialize("abc")

        serialized = msgpack.unpackb(buffer.getvalue(), strict_map_key=False)
        self.assertEqual(
            serialized,
            {
                TYPE_TAG: TYPE_ID_STRING,
                VALUE_TAG: "abc"
            })

    def test_deserialize_str(self):
        deserializer = self.create_deserializer()

        deserialized = deserializer.deserialize({TYPE_TAG: TYPE_ID_STRING, VALUE_TAG: "abc"})

        self.assertEqual(deserialized, "abc")

    def test_serialize_file_path(self):
        serializer, buffer = self.create_serializer_and_buffer("a/e/f.bin")

        serializer.serialize(FilePath.relative("a/b/c/d.txt"))

        serialized = msgpack.unpackb(buffer.getvalue(), strict_map_key=False)
        self.assertEqual(
            serialized,
            {
                TYPE_TAG: TYPE_ID_FILE_PATH,
                VALUE_TAG: [True, "../b/c/d.txt"]
            })

    def test_deserialize_file_path(self):
        deserializer = self.create_deserializer("a/e/f.bin")

        deserialized = deserializer.deserialize(
            {
                TYPE_TAG: TYPE_ID_FILE_PATH,
                VALUE_TAG: [True, "../b/c/d.txt"]
            }
        )

        self.assertEqual(deserialized, FilePath.relative("a/b/c/d.txt"))

    def test_serialize_cache_key(self):
        serializer, buffer = self.create_serializer_and_buffer("a/e/f.bin")

        serializer.serialize(
            CacheKey.Builder()
            .set_protocol("123")
            .add_string_part("abc")
            .add_file_path_part(FilePath.relative("a/b/c/d.txt"))
            .build())

        serialized = msgpack.unpackb(buffer.getvalue(), strict_map_key=False)
        self.assertEqual(
            serialized,
            {
                TYPE_TAG: TYPE_ID_CACHE_KEY,
                VALUE_TAG: [
                    "123",
                    [
                        {TYPE_TAG: TYPE_ID_STRING, VALUE_TAG: "abc"},
                        {TYPE_TAG: TYPE_ID_FILE_PATH, VALUE_TAG: [True, "../b/c/d.txt"]},
                    ]
                ]
            })

    def test_deserialize_cache_key(self):
        deserializer = self.create_deserializer("a/e/f.bin")

        deserialized = deserializer.deserialize(
            {
                TYPE_TAG: TYPE_ID_CACHE_KEY,
                VALUE_TAG: [
                    "123",
                    [
                        {TYPE_TAG: TYPE_ID_STRING, VALUE_TAG: "abc"},
                        {TYPE_TAG: TYPE_ID_FILE_PATH, VALUE_TAG: [True, "../b/c/d.txt"]},
                    ]
                ]
            }
        )

        self.assertEqual(
            deserialized,
            CacheKey.Builder()
            .set_protocol("123")
            .add_string_part("abc")
            .add_file_path_part(FilePath.relative("a/b/c/d.txt"))
            .build())

    def test_serialize_cached(self):
        serializer, buffer = self.create_serializer_and_buffer()

        serializer.serialize(
            Cached.of(
                CacheKey.Builder()
                .set_protocol("123")
                .add_string_part("abc")
                .build()))

        serialized = msgpack.unpackb(buffer.getvalue(), strict_map_key=False)
        self.assertEqual(
            serialized,
            {
                TYPE_TAG: TYPE_ID_CACHED,
                VALUE_TAG: {
                    TYPE_TAG: TYPE_ID_CACHE_KEY,
                    VALUE_TAG: ["123", [{TYPE_TAG: TYPE_ID_STRING, VALUE_TAG: "abc"}]]
                }
            })

    def test_deserialize_cached(self):
        deserializer = self.create_deserializer()

        deserialized = deserializer.deserialize(
            {
                TYPE_TAG: TYPE_ID_CACHED,
                VALUE_TAG: {
                    TYPE_TAG: TYPE_ID_CACHE_KEY,
                    VALUE_TAG: ["123", [{TYPE_TAG: TYPE_ID_STRING, VALUE_TAG: "abc"}]]
                }
            }
        )

        self.assertEqual(
            deserialized,
            Cached.of(
                CacheKey.Builder()
                .set_protocol("123")
                .add_string_part("abc")
                .build()))

    def test_serialize_HahaMapEntry(self):
        serializer, buffer = self.create_serializer_and_buffer()

        serializer.serialize(HanaMapEntry("abc", numpy.int32(10)))

        serialized = msgpack.unpackb(buffer.getvalue(), strict_map_key=False)
        self.assertEqual(
            serialized,
            {
                TYPE_TAG: TYPE_ID_HANA_MAP_ENTRY,
                VALUE_TAG: [
                    {
                        TYPE_TAG: TYPE_ID_STRING,
                        VALUE_TAG: "abc"
                    },
                    {
                        TYPE_TAG: TYPE_ID_INTEGER,
                        VALUE_TAG: 10
                    }
                ]
            })

    def test_deserialize_HanaMapEntry(self):
        deserializer = self.create_deserializer()

        deserialized = deserializer.deserialize(
            {
                TYPE_TAG: TYPE_ID_HANA_MAP_ENTRY,
                VALUE_TAG: [
                    {
                        TYPE_TAG: TYPE_ID_STRING,
                        VALUE_TAG: "abc"
                    },
                    {
                        TYPE_TAG: TYPE_ID_INTEGER,
                        VALUE_TAG: 10
                    }
                ]
            }
        )

        self.assertEqual(deserialized, HanaMapEntry("abc", numpy.int32(10)))


def define_test_suite(suite: TestSuite):
    suite.addTest(unittest.makeSuite(PrimitiveReadableSerializationTest))
    suite.addTest(unittest.makeSuite(PrimitiveBinarySerializationTest))


if __name__ == "__main__":
    unittest.main()
