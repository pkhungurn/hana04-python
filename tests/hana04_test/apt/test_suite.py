from unittest import TestSuite

import hana04_test.apt.caching.test_suite
import hana04_test.apt.extensible.test_suite


def define_test_suite(suite: TestSuite):
    hana04_test.apt.caching.test_suite.define_test_suite(suite)
    hana04_test.apt.extensible.test_suite.define_test_suite(suite)
