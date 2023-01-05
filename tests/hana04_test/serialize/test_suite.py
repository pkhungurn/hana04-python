from unittest import TestSuite

import hana04_test.serialize.extensible.test_suite
import hana04_test.serialize.primitive.test_suite


def define_test_suite(suite: TestSuite):
    hana04_test.serialize.extensible.test_suite.define_test_suite(suite)
    hana04_test.serialize.primitive.test_suite.define_test_suite(suite)
