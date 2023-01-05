from unittest import TestSuite

import hana04_test.apt.extensible.hana_customized_builder_decorators_test
import hana04_test.apt.extensible.hana_extension_decorators_test
import hana04_test.apt.extensible.hana_interface_decorators_test
import hana04_test.apt.extensible.hana_late_deserializable_decorators_test
import hana04_test.apt.extensible.hana_object_decorators_test
import hana04_test.apt.extensible.property_type_spec_test


def define_test_suite(suite: TestSuite):
    hana04_test.apt.extensible.hana_customized_builder_decorators_test.define_test_suite(suite)
    hana04_test.apt.extensible.hana_extension_decorators_test.define_test_suite(suite)
    hana04_test.apt.extensible.hana_interface_decorators_test.define_test_suite(suite)
    hana04_test.apt.extensible.hana_late_deserializable_decorators_test.define_test_suite(suite)
    hana04_test.apt.extensible.hana_object_decorators_test.define_test_suite(suite)
    hana04_test.apt.extensible.property_type_spec_test.define_test_suite(suite)

