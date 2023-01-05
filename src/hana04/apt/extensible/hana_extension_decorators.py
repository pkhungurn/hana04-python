import inspect
from typing import Optional

from hana04.apt.extensible.hana_meta import HanaMeta, hana_meta
from hana04.base.extension.hana_extension_factory import HanaExtensionFactory
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import is_class_injectable, injectable_class
from jyuusu.factory_resolver import has_injectable_factory, make_injectable_factory, factory_class


def add_hana_extension_module(factory_class: type, extension_class: type, extensible_class: type):
    assert extension_class is not None
    assert extensible_class is not None
    HanaMeta.assert_is_hana_interface(extensible_class)
    extensible_meta = hana_meta(extensible_class)
    extension_factory_class = extensible_meta.extension_factory_class
    assert issubclass(factory_class, extension_factory_class)
    if not is_class_injectable(factory_class):
        injectable_class(factory_class)

    class _HanaExtensionModule(JyuusuModule):
        def configure(self, binder: Binder):
            binder.install_class(factory_class)
            binder.install_module(extensible_meta.module)
            binder.bind_to_dict(type, extensible_meta.extension_factory_class) \
                .with_key(extension_class) \
                .to_type(factory_class)

    factory_class._HanaExtensionModule = _HanaExtensionModule
    return factory_class


def assert_only_name_unassigned_args(full_arg_spec: inspect.FullArgSpec):
    assert full_arg_spec.varargs is None
    assert full_arg_spec.varkw is None
    assert full_arg_spec.defaults is None
    assert full_arg_spec.kwonlyargs == []
    assert full_arg_spec.kwonlydefaults is None


def extract_hana_extension_spec_from_factory_class(cls):
    assert inspect.isclass(cls)
    assert issubclass(cls, HanaExtensionFactory)
    assert "create" in cls.__dict__
    create_method = cls.__dict__["create"]
    create_arg_spec = inspect.getfullargspec(create_method)
    assert_only_name_unassigned_args(create_arg_spec)
    assert len(create_arg_spec.args) == 2
    assert create_arg_spec.args[0] == 'self'

    if 'return' in create_arg_spec.annotations:
        extension_class = create_arg_spec.annotations['return']
        assert inspect.isclass(extension_class)
    else:
        extension_class = None

    if create_arg_spec.args[1] in create_arg_spec.annotations:
        extensible_class = create_arg_spec.annotations[create_arg_spec.args[1]]
        assert inspect.isclass(extensible_class)
    else:
        extensible_class = None

    return extension_class, extensible_class


def hana_extension_factory_with_manual_spec(
        extension_class: Optional[type] = None,
        extensible_class: Optional[type] = None):
    def _add_hana_extension_module(cls):
        extracted_extension_class, extracted_extensible_class = extract_hana_extension_spec_from_factory_class(cls)
        if extension_class is None:
            extension_class_to_use = extracted_extension_class
        else:
            extension_class_to_use = extension_class
        if extensible_class is None:
            extensible_class_to_use = extracted_extensible_class
        else:
            extensible_class_to_use = extensible_class
        add_hana_extension_module(cls, extension_class_to_use, extensible_class_to_use)
        return cls

    return _add_hana_extension_module


def hana_extension_factory(cls):
    extension_class, extensible_class = extract_hana_extension_spec_from_factory_class(cls)
    add_hana_extension_module(cls, extension_class, extensible_class)
    return cls


def hana_extension_module(cls):
    assert "_HanaExtensionModule" in cls.__dict__
    return cls._HanaExtensionModule


def extract_hana_extension_spec_from_extension_class(cls):
    assert inspect.isclass(cls)
    assert "__init__" in cls.__dict__
    init_arg_spec = inspect.getfullargspec(cls.__init__)
    assert_only_name_unassigned_args(init_arg_spec)
    assert len(init_arg_spec.args) >= 2
    assert init_arg_spec.args[0] == 'self'

    extension_class = cls.__bases__[0]
    if extension_class == object:
        extension_class = None

    if init_arg_spec.args[1] in init_arg_spec.annotations:
        extensible_class = init_arg_spec.annotations[init_arg_spec.args[1]]
        assert inspect.isclass(extensible_class)
    else:
        extensible_class = None

    return extension_class, extensible_class


def make_hana_extension_out_of(cls: type, extension_class: type, extensible_class: type):
    assert extension_class is not None
    assert extensible_class is not None
    HanaMeta.assert_is_hana_interface(extensible_class)
    extensible_meta = hana_meta(extensible_class)
    init_arg_spec = inspect.getfullargspec(cls.__init__)

    if not has_injectable_factory(cls):
        if len(init_arg_spec.args) == 2:
            resolved_start = None
        else:
            resolved_start = init_arg_spec.args[2]
        make_injectable_factory(cls, resolved_start)

    extension_factory_class = factory_class(cls)

    @hana_extension_factory_with_manual_spec(extension_class, extensible_class)
    class _HanaExtensionFactory(extensible_meta.extension_factory_class):
        def __init__(self, factory: extension_factory_class):
            self.factory = factory

        def create(self, extensible):
            return self.factory.create(extensible)

    class _HanaExtensionModule(JyuusuModule):
        def configure(self, binder: Binder):
            binder.install_class(extension_factory_class)
            binder.install_module(hana_extension_module(_HanaExtensionFactory))

    cls.HanaExtensionFactory = _HanaExtensionFactory
    cls._HanaExtensionModule = _HanaExtensionModule
    return cls


def hana_extension_with_manual_spec(
        extension_class: Optional[type] = None,
        extensible_class: Optional[type] = None):
    def func(cls):
        extracted_extension_class, extracted_extensible_class = extract_hana_extension_spec_from_extension_class(cls)
        if extension_class is None:
            extension_class_to_use = extracted_extension_class
        else:
            extension_class_to_use = extension_class
        if extensible_class is None:
            extensible_class_to_use = extracted_extensible_class
        else:
            extensible_class_to_use = extensible_class
        make_hana_extension_out_of(cls, extension_class_to_use, extensible_class_to_use)

        return cls

    return func


def hana_extension(cls):
    extracted_extension_class, extracted_extensible_class = extract_hana_extension_spec_from_extension_class(cls)
    make_hana_extension_out_of(cls, extracted_extension_class, extracted_extensible_class)
    return cls
