from unittest import TestSuite

import hana04_test.serialize.primitive.primitive_serialization_test


def define_test_suite(suite: TestSuite):
    hana04_test.serialize.primitive.primitive_serialization_test.define_test_suite(suite)