import inspect
from abc import abstractmethod

import numpy

from hana04.apt.extensible.constants import HANA_META_PROPERTY_NAME
from hana04.apt.extensible.hana_meta import HanaMeta
from hana04.base.extension.hana_object import HanaObject


def hana_interface(cls):
    HanaMeta.assert_hana_interface_can_be_created(cls)
    hana_meta: HanaMeta = cls.__dict__[HANA_META_PROPERTY_NAME]
    hana_meta.make_hana_interface(cls)
    return cls


def hana_abstract_property(property_):
    full_arg_spec = inspect.getfullargspec(property_)
    assert len(full_arg_spec.annotations) == 1
    assert 'return' in full_arg_spec.annotations
    assert len(full_arg_spec.args) == 1
    assert full_arg_spec.varargs == None
    assert full_arg_spec.varkw == None
    assert full_arg_spec.defaults == None
    assert len(full_arg_spec.kwonlyargs) == 0
    assert full_arg_spec.kwonlydefaults is None
    return property(abstractmethod(property_))


if __name__ == "__main__":
    @hana_interface
    class AnInterface(HanaObject):
        _HANA_META = HanaMeta()

        @hana_abstract_property
        def intField(self) -> numpy.int32:
            pass

        @hana_abstract_property
        def longField(self) -> numpy.int64:
            pass

        @hana_abstract_property
        def floatField(self) -> numpy.float32:
            pass

        @hana_abstract_property
        def doubleField(self) -> numpy.float64:
            pass


    print(AnInterface._HANA_META.class_name)
    print(AnInterface._HANA_META.extension_factory_class)
    print(AnInterface._HANA_META.parent_class)
    print(AnInterface._HANA_META.interface_module)
