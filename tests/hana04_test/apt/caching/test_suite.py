from unittest import TestSuite

import hana04_test.apt.caching.hana_cache_loader_decorators_test


def define_test_suite(suite: TestSuite):
    hana04_test.apt.caching.hana_cache_loader_decorators_test.define_test_suite(suite)