import unittest
from typing import Optional, ForwardRef, List
from unittest import TestCase, TestSuite

import numpy

from hana04.base.caching.wrapped import Wrapped
from hana04.apt.extensible.property_type_spec import PropertyTypeSpec, TerminalTypeSpec, WrappedTypeSpec, \
    OptionalTypeSpec, ListTypeSpec


class PropertyTypeSpecTest(TestCase):
    def test_HanaProperty_parse_terminal_spec(self):
        result = PropertyTypeSpec.create(numpy.int32)

        self.assertTrue(result, TerminalTypeSpec(numpy.int32))

    def test_parse_terminal_spec_ForwardRef(self):
        result = PropertyTypeSpec.create(ForwardRef('Something'))

        self.assertTrue(result, TerminalTypeSpec(ForwardRef('Something')))

    def test_parse_warpped_spec(self):
        result = PropertyTypeSpec.create(Wrapped[numpy.int32])

        self.assertTrue(result, WrappedTypeSpec(TerminalTypeSpec(numpy.int32)))

    def test_parse_optional_spec(self):
        result = PropertyTypeSpec.create(Optional[numpy.int32])

        self.assertEqual(result, OptionalTypeSpec(TerminalTypeSpec(numpy.int32)))

    def test_parse_list_spec(self):
        result = PropertyTypeSpec.create(List[numpy.int32])

        self.assertEqual(result, ListTypeSpec(TerminalTypeSpec(numpy.int32)))

    def test_parse_list_wrapped_spec(self):
        result = PropertyTypeSpec.create(List[Wrapped[numpy.int32]])

        self.assertEqual(result, ListTypeSpec(WrappedTypeSpec(TerminalTypeSpec(numpy.int32))))


def define_test_suite(suite: TestSuite):
    suite.addTest(unittest.makeSuite(PropertyTypeSpecTest))


if __name__ == "__main__":
    unittest.main()
