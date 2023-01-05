import unittest
from abc import abstractmethod
from unittest import TestCase, TestSuite

import numpy

from hana04.apt.extensible.hana_interface_decorators import hana_interface
from hana04.apt.extensible.hana_meta import HanaMeta
from hana04.base.extension.hana_object import HanaObject


class HanaInterfaceDecoratorsTest(TestCase):
    def test01(self):
        @hana_interface
        class AnInterface(HanaObject):
            _HANA_META = HanaMeta()

            @property
            @abstractmethod
            def intField(self) -> numpy.int32:
                pass

            @property
            @abstractmethod
            def longField(self) -> numpy.int64:
                pass

            @property
            @abstractmethod
            def floatField(self) -> numpy.float32:
                pass

            @property
            @abstractmethod
            def doubleField(self) -> numpy.float64:
                pass


def define_test_suite(suite: TestSuite):
    suite.addTest(unittest.makeSuite(HanaInterfaceDecoratorsTest))


if __name__ == "__main__":
    unittest.main()
