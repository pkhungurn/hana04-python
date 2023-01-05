import unittest
from typing import Optional, List, Dict
from unittest import TestCase, TestSuite

from hana04.base.module import HanaBaseModule
from hana04.serialize.module import HanaSerializeModule
from hana04.apt.extensible.hana_meta import hana_module
from hana04.apt.extensible.hana_object_decorators import hana_object, hana_property
from hana04.apt.extensible.hana_object_meta import HanaObjectMeta
from hana04.base.caching.wrapped import Wrapped
from hana04.base.changeprop.variable import Variable
from hana04.base.extension.hana_object import HanaObject
from jyuusu.injectors import create_injector


@hana_object
class Aaa(HanaObject):
    _HANA_META = HanaObjectMeta(
        type_id=-10010,
        type_names=["base.decorators.Aaa"])

    @hana_property(_HANA_META, 1)
    def stringField(self) -> str:
        pass

    @hana_property(_HANA_META, 2)
    def wrappedStringField(self) -> Wrapped[str]:
        pass

    @hana_property(_HANA_META, 3)
    def optionalStringField(self) -> Optional[str]:
        pass

    @hana_property(_HANA_META, 4)
    def stringListField(self) -> List[str]:
        pass

    @hana_property(_HANA_META, 5)
    def stringBooleanMapField(self) -> Dict[str, bool]:
        pass

    @hana_property(_HANA_META, 6)
    def varStringField(self) -> Variable[str]:
        pass

    @hana_property(_HANA_META, 7)
    def varStringListField(self) -> Variable[List[str]]:
        pass


class HanaObjectDecoratorTest(TestCase):
    def setUp(self) -> None:
        self.injector = create_injector(
            HanaBaseModule,
            HanaSerializeModule,
            hana_module(Aaa))

    def test_default_builder(self):
        builder = self.injector.get_instance(Aaa._HANA_META.default_builder_class)

        instance = builder \
            .setStringField("abc") \
            .setWrappedStringField("bcd") \
            .addStringListField("1") \
            .addStringListField("2") \
            .putStringBooleanMapField("a", True) \
            .putStringBooleanMapField("b", False) \
            .setVarStringField("xyz") \
            .addVarStringListField("i", "ii", "iii") \
            .build()

        self.assertEqual(instance.stringField(), "abc")
        self.assertEqual(instance.wrappedStringField().value, "bcd")
        self.assertEqual(instance.optionalStringField(), None)
        self.assertEqual(instance.stringListField(), ["1", "2"])
        self.assertEqual(instance.stringBooleanMapField(), {"a": True, "b": False})
        self.assertEqual(instance.varStringField().value(), "xyz")
        self.assertEqual(instance.varStringListField().value(), ["i", "ii", "iii"])

        with instance.varStringListField().mutate() as list_val:
            list_val.append("iv")

        self.assertEqual(instance.varStringListField().value(), ["i", "ii", "iii", "iv"])


def define_test_suite(suite: TestSuite):
    suite.addTest(unittest.makeSuite(HanaObjectDecoratorTest))


if __name__ == "__main__":
    unittest.main()
