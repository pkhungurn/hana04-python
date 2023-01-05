from hana04.apt.extensible.constants import HANA_META_PROPERTY_NAME
from hana04.apt.extensible.hana_late_deserializable_meta import HanaLateDeserializableMeta


def hana_late_deserializable(cls):
    HanaLateDeserializableMeta.assert_hana_object_can_be_created(cls)
    hana_meta: HanaLateDeserializableMeta = cls.__dict__[HANA_META_PROPERTY_NAME]
    hana_meta.make_hana_late_deserializable(cls)
    return cls
