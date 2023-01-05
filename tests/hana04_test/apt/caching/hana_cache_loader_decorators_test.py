import unittest
from unittest import TestSuite

from hana04.apt.caching.hana_cache_loader_decorators import hana_cache_loader, hana_cache_loader_module
from hana04.base.caching.cache_key import CacheKey, StringCacheKeyPart
from hana04.base.caching.hana_cache_loader import HanaCacheLoader
from hana04.base.caching.wrapped import HanaUnwrapper, Cached
from jyuusu.constructor_resolver import injectable_class, memoized
from jyuusu.injectors import create_injector

from hana04.base.module import HanaBaseModule
from hana04.serialize.module import HanaSerializeModule


@hana_cache_loader("StringLoader")
@memoized
@injectable_class
class StringCacheLoader(HanaCacheLoader):

    def load(self, key: CacheKey) -> str:
        assert key.protocol == "StringLoader"
        assert len(key.parts)
        assert isinstance(key.parts[0], StringCacheKeyPart)
        return key.parts[0].value


class HanaCacheLoaderDecoratorsTest(unittest.TestCase):
    def setUp(self):
        self.injector = create_injector(
            HanaBaseModule,
            HanaSerializeModule,
            hana_cache_loader_module(StringCacheLoader))

    def test_unwrap(self):
        unwrapper: HanaUnwrapper = self.injector.get_instance(HanaUnwrapper)

        value = unwrapper.unwrap(Cached.of(CacheKey.Builder("StringLoader").add_string_part("123").build()))

        self.assertEqual(value, "123")


def define_test_suite(suite: TestSuite):
    suite.addTest(unittest.makeSuite(HanaCacheLoaderDecoratorsTest))


if __name__ == "__main__":
    unittest.main()
