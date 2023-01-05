import unittest
from abc import ABC, abstractmethod
from unittest import TestSuite

from hana04.base.module import HanaBaseModule
from hana04.serialize.module import HanaSerializeModule
from hana04.apt.extensible.hana_extension_decorators import hana_extension_factory, hana_extension_module, \
    hana_extension_factory_with_manual_spec, hana_extension_with_manual_spec, hana_extension
from hana04.apt.extensible.hana_meta import hana_meta
from hana04.apt.extensible.hana_object_decorators import hana_object
from hana04.apt.extensible.hana_object_meta import HanaObjectMeta, hana_object_meta
from hana04.base.extension.hana_object import HanaObject
from jyuusu.constructor_resolver import injectable_class
from jyuusu.injectors import create_injector


@hana_object
class Aaa(HanaObject):
    _HANA_META = HanaObjectMeta(
        type_id=-10010,
        type_names=["Aaa"])


class Extension00:
    def __init__(self, aaa: Aaa):
        self.aaa = aaa

    def something(self):
        return 10


@hana_extension_factory
class AaaExtension00Factory(hana_meta(Aaa).extension_factory_class):
    def create(self, extensible: Aaa) -> Extension00:
        return Extension00(extensible)


class Extension01:
    def __init__(self, aaa: Aaa):
        self.aaa = aaa

    def something(self):
        return 20


@hana_extension_factory_with_manual_spec(Extension01, Aaa)
class AaaExtension01Factory(hana_meta(Aaa).extension_factory_class):
    def create(self, extensible):
        return Extension01(extensible)


class Extension02:
    def __init__(self, aaa: Aaa):
        self.aaa = aaa

    def something(self):
        return 30


@hana_extension_with_manual_spec(Extension02, Aaa)
class Extension02ForAaa(Extension02):
    def __init__(self, aaa):
        super().__init__(aaa)


@injectable_class
class Foo:
    def bar(self):
        return 0


class Extension03(ABC):
    def __init__(self, aaa: Aaa, foo: Foo):
        self.foo = foo
        self.aaa = aaa

    @abstractmethod
    def something(self):
        pass


@hana_extension
class Extension03ForAaa(Extension03):
    def __init__(self, aaa: Aaa, foo: Foo):
        super().__init__(aaa, foo)

    def something(self):
        return 40


class HanaExtensionDecoratorsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.injector = create_injector(
            HanaBaseModule,
            HanaSerializeModule,
            hana_meta(Aaa).module,
            hana_extension_module(AaaExtension00Factory),
            hana_extension_module(AaaExtension01Factory),
            hana_extension_module(Extension02ForAaa),
            hana_extension_module(Extension03ForAaa))

    def test_hana_enxtension_factory(self):
        aaa: Aaa = self.injector.get_instance(hana_object_meta(Aaa).default_builder_class).build()

        self.assertFalse(aaa.has_extension(Extension00))
        self.assertTrue(aaa.supports_extension(Extension00))

        extension_00: Extension00 = aaa.get_extension(Extension00)

        self.assertTrue(aaa.has_extension(Extension00))
        self.assertEqual(extension_00.aaa, aaa)
        self.assertEqual(extension_00.something(), 10)

    def test_hana_extension_factory_with_manual_spec(self):
        aaa: Aaa = self.injector.get_instance(hana_object_meta(Aaa).default_builder_class).build()

        self.assertFalse(aaa.has_extension(Extension01))
        self.assertTrue(aaa.supports_extension(Extension01))

        extension_01: Extension01 = aaa.get_extension(Extension01)

        self.assertTrue(aaa.has_extension(Extension01))
        self.assertEqual(extension_01.aaa, aaa)
        self.assertEqual(extension_01.something(), 20)

    def test_hana_extension_with_manual_spec(self):
        aaa: Aaa = self.injector.get_instance(hana_object_meta(Aaa).default_builder_class).build()

        self.assertFalse(aaa.has_extension(Extension02))
        self.assertTrue(aaa.supports_extension(Extension02))

        extension_02: Extension02 = aaa.get_extension(Extension02)

        self.assertTrue(aaa.has_extension(Extension02))
        self.assertEqual(extension_02.aaa, aaa)
        self.assertEqual(extension_02.something(), 30)

    def test_hana_extension(self):
        aaa: Aaa = self.injector.get_instance(hana_object_meta(Aaa).default_builder_class).build()

        self.assertFalse(aaa.has_extension(Extension03))
        self.assertTrue(aaa.supports_extension(Extension03))

        extension_03: Extension03 = aaa.get_extension(Extension03)

        self.assertTrue(aaa.has_extension(Extension03))
        self.assertEqual(extension_03.aaa, aaa)
        self.assertEqual(extension_03.something(), 40)
        self.assertEqual(extension_03.foo.bar(), 0)


def define_test_suite(suite: TestSuite):
    suite.addTest(unittest.makeSuite(HanaExtensionDecoratorsTest))


if __name__ == "__main__":
    unittest.main()
