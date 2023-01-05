import inspect

from hana04.base.serialize.binary.binary_deserializer import TypeBinaryDeserializer, BinaryDeserializer
from hana04.base.serialize.binary.binary_serializer import TypeBinarySerializer, BinarySerializer
from hana04.base.serialize.readable.readable_deserializer import TypeReadableDeserializer, ReadableDeserializer
from hana04.base.serialize.readable.readable_serializer import TypeReadableSerializer, ReadableSerializer
from jyuusu.binder import Binder, Module as JyuusuModule
from jyuusu.constructor_resolver import is_class_injectable, injectable_class


def hana_binary_deserializer(type_id: int):
    def the_func(cls):
        assert inspect.isclass(cls)
        assert issubclass(cls, TypeBinaryDeserializer)
        if not is_class_injectable(cls):
            injectable_class(cls)

        class _HanaBinaryDeserializerModule(JyuusuModule):
            def configure(self, binder: Binder):
                binder.install_module(BinaryDeserializer.Module)
                binder.install_class(cls)
                binder.bind_to_dict(int, TypeBinaryDeserializer).with_key(type_id).to_type(cls)

        cls._HanaBinaryDeserializerModule = _HanaBinaryDeserializerModule

        return cls

    return the_func


def hana_binary_deserializer_module(cls):
    assert "_HanaBinaryDeserializerModule" in cls.__dict__
    return cls._HanaBinaryDeserializerModule


def hana_binary_serializer_by_type_id(type_id: int):
    """Use this only on subclasses of HanaExtensible."""

    def the_func(cls):
        assert inspect.isclass(cls)
        assert issubclass(cls, TypeBinarySerializer)
        if not is_class_injectable(cls):
            injectable_class(cls)

        class _HanaBinarySerializerModule(JyuusuModule):
            def configure(self, binder: Binder):
                binder.install_module(BinarySerializer.Module)
                binder.install_class(cls)
                binder.bind_to_dict(int, TypeBinarySerializer).with_key(type_id).to_type(cls)

        cls._HanaBinarySerializerModule = _HanaBinarySerializerModule

        return cls

    return the_func


def hana_binary_serializer_by_type(type_: type):
    """Use this on value types."""

    def the_func(cls):
        assert inspect.isclass(cls)
        assert issubclass(cls, TypeBinarySerializer)
        if not is_class_injectable(cls):
            injectable_class(cls)

        class _HanaBinarySerializerModule(JyuusuModule):
            def configure(self, binder: Binder):
                binder.install_module(BinarySerializer.Module)
                binder.install_class(cls)
                binder.bind_to_dict(type, TypeBinarySerializer).with_key(type_).to_type(cls)

        cls._HanaBinarySerializerModule = _HanaBinarySerializerModule

        return cls

    return the_func


def hana_binary_serializer_module(cls):
    assert '_HanaBinarySerializerModule' in cls.__dict__
    return cls._HanaBinarySerializerModule


def hana_readable_deserializer(*type_names):
    for type_name in type_names:
        assert isinstance(type_name, str)

    def the_func(cls):
        assert inspect.isclass(cls)
        assert issubclass(cls, TypeReadableDeserializer)
        if not is_class_injectable(cls):
            injectable_class(cls)

        class _HanaReadableDeserializerModule(JyuusuModule):
            def configure(self, binder: Binder):
                binder.install_module(ReadableDeserializer.Module)
                binder.install_class(cls)
                for type_name in type_names:
                    binder.bind_to_dict(str, TypeReadableDeserializer).with_key(type_name).to_type(cls)

        cls._HanaReadableDeserializerModule = _HanaReadableDeserializerModule

        return cls

    return the_func


def hana_readable_deserializer_module(cls):
    assert '_HanaReadableDeserializerModule' in cls.__dict__
    return cls._HanaReadableDeserializerModule


def hana_readable_serializer_by_type_name(*type_names):
    """Use this only on subclasses of HanaExtensible."""

    for type_name in type_names:
        assert isinstance(type_name, str)

    def the_func(cls):
        assert inspect.isclass(cls)
        assert issubclass(cls, TypeReadableSerializer)
        if not is_class_injectable(cls):
            injectable_class(cls)

        class _HanaReadableSerializerModule(JyuusuModule):
            def configure(self, binder: Binder):
                binder.install_module(ReadableSerializer.Module)
                binder.install_class(cls)
                for type_name in type_names:
                    binder.bind_to_dict(str, TypeReadableSerializer).with_key(type_name).to_type(cls)

        cls._HanaReadableSerializerModule = _HanaReadableSerializerModule

        return cls

    return the_func


def hana_readable_serializer_by_type(type_: type):
    """Use this on value types."""

    def the_func(cls):
        assert inspect.isclass(cls)
        assert issubclass(cls, TypeReadableSerializer)
        if not is_class_injectable(cls):
            injectable_class(cls)

        class _HanaReadableSerializerModule(JyuusuModule):
            def configure(self, binder: Binder):
                binder.install_module(ReadableSerializer.Module)
                binder.install_class(cls)
                binder.bind_to_dict(type, TypeReadableSerializer).with_key(type_).to_type(cls)

        cls._HanaReadableSerializerModule = _HanaReadableSerializerModule

        return cls

    return the_func


def hana_readable_serializer_module(cls):
    assert '_HanaReadableSerializerModule' in cls.__dict__
    return cls._HanaReadableSerializerModule
