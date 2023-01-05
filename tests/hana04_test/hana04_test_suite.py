import unittest
from unittest import TestSuite

import hana04_test.apt.test_suite
import hana04_test.serialize.test_suite


def define_test_suite(suite: TestSuite):
    hana04_test.apt.test_suite.define_test_suite(suite)
    hana04_test.serialize.test_suite.define_test_suite(suite)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    define_test_suite(suite)
    runner = unittest.TextTestRunner()
    runner.run(suite)
