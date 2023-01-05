import inspect

from hana04.apt.extensible.constants import HANA_META_PROPERTY_NAME
from hana04.apt.extensible.hana_object_meta import HanaObjectMeta
from hana04.base.extension.constants import HANA_CUSTOMIZED_BUILDER_TAG
from hana04.base.extension.fluent_builder import FluentBuilderFactory, FluentBuilder
from hana04.base.extension.hana_customized_builders import HanaCustomizedBuilderModule
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import is_class_injectable, injectable_class, memoized
from jyuusu.provider import Provider


def hana_customized_builder(hana_object_class: type):
    HanaObjectMeta.assert_hana_object_can_be_created(hana_object_class)
    hana_object_meta: HanaObjectMeta = hana_object_class.__dict__[HANA_META_PROPERTY_NAME]
    assert hana_object_meta.owning_class is not None

    def func(builder_class):
        inspect.isclass(builder_class)
        assert issubclass(builder_class, hana_object_meta.default_builder_class)
        if not is_class_injectable(builder_class):
            injectable_class(builder_class)

        @memoized
        @injectable_class
        class _HanaFluentBuilderFactory(FluentBuilderFactory):
            def __init__(self, builder_provider: Provider[builder_class]):
                self.builder_provider = builder_provider

            def create(self) -> FluentBuilder:
                return self.builder_provider.get()

        builder_class._HanaFluentBuilderFactory = _HanaFluentBuilderFactory

        class _HanaCustomizedBuilderModule(JyuusuModule):
            def configure(self, binder: Binder):
                binder.install_class(builder_class)
                binder.install_module(HanaCustomizedBuilderModule)
                binder.install_class(_HanaFluentBuilderFactory)
                binder.bind_to_dict(type, FluentBuilderFactory, HANA_CUSTOMIZED_BUILDER_TAG) \
                    .with_key(hana_object_class) \
                    .to_type(_HanaFluentBuilderFactory)

        builder_class._HanaCustomizedBuilderModule = _HanaCustomizedBuilderModule

        return builder_class

    return func


def hana_customized_builder_module(cls):
    return cls._HanaCustomizedBuilderModule
