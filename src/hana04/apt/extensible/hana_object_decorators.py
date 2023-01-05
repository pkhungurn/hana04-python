import inspect
from abc import abstractmethod

from hana04.apt.extensible.constants import HANA_META_PROPERTY_NAME
from hana04.apt.extensible.property_type_spec import PropertyTypeSpec
from hana04.apt.extensible.hana_property_spec import HanaPropertySpec
from hana04.apt.extensible.hana_object_meta import HanaObjectMeta


def hana_property(hana_object_meta: HanaObjectMeta, property_id: int):
    def func(property_):
        full_arg_spec = inspect.getfullargspec(property_)
        assert len(full_arg_spec.annotations) == 1
        assert 'return' in full_arg_spec.annotations
        assert len(full_arg_spec.args) == 1
        assert full_arg_spec.varargs == None
        assert full_arg_spec.varkw == None
        assert full_arg_spec.defaults == None
        assert len(full_arg_spec.kwonlyargs) == 0
        assert full_arg_spec.kwonlydefaults is None
        hana_object_meta.add_property(
            HanaPropertySpec(
                property_.__name__,
                property_id,
                PropertyTypeSpec.create(full_arg_spec.annotations['return'])))

        return abstractmethod(property_)

    return func


def hana_object(cls):
    HanaObjectMeta.assert_hana_object_can_be_created(cls)
    hana_object_meta: HanaObjectMeta = cls.__dict__[HANA_META_PROPERTY_NAME]
    hana_object_meta.make_hana_object(cls)
    return cls
