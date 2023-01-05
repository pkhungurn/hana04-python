from typing import Dict, Optional

from hana04.base.extension.constants import HANA_CUSTOMIZED_BUILDER_TAG
from hana04.base.extension.fluent_builder import FluentBuilderFactory, FluentBuilder
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import injectable_class_with_specs, memoized


@memoized
@injectable_class_with_specs(type_to_builder_factory=HANA_CUSTOMIZED_BUILDER_TAG)
class HanaCustomizedBuilders:
    def __init__(self, type_to_builder_factory: Dict[type, FluentBuilderFactory]):
        self.type_to_builder_factory = type_to_builder_factory

    def get_factory(self, type_: type) -> Optional[FluentBuilderFactory]:
        if type_ not in self.type_to_builder_factory:
            return None
        else:
            return self.type_to_builder_factory[type_]

    def get(self, type_: type) -> Optional[FluentBuilder]:
        if type_ not in self.type_to_builder_factory:
            return None
        else:
            return self.type_to_builder_factory[type_].create()


class HanaCustomizedBuilderModule(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_dict(type, FluentBuilderFactory, tag=HANA_CUSTOMIZED_BUILDER_TAG)
        binder.install_class(HanaCustomizedBuilders)
