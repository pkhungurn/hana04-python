from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from hana04.base.filesystem.file_path import FilePath


class CacheKeyPart(ABC):
    @abstractmethod
    def get_string_part(self):
        pass


@dataclass(eq=True)
class StringCacheKeyPart(CacheKeyPart):
    value: str

    def get_string_part(self):
        return f"String:::{self.value}"


@dataclass(eq=True)
class FilePathCacheKeyPart(CacheKeyPart):
    value: FilePath

    def get_string_part(self):
        return f"FilePath:::{self.value.stored_path}"


class CacheKey:
    SEPARATOR = "|||||"

    def __init__(self, protocol: str, parts: List[CacheKeyPart], string_key: str):
        self._string_key = string_key
        self._parts = parts
        self._protocol = protocol

    @property
    def string_key(self):
        return self._string_key

    @property
    def parts(self):
        return self._parts

    @property
    def protocol(self):
        return self._protocol

    def __eq__(self, other):
        if not isinstance(other, CacheKey):
            return False
        return self._protocol == other._protocol and self._parts == other._parts

    def __repr__(self):
        return f"CacheKey(protocol={self.protocol}, {self.parts})"

    class Builder:
        def __init__(self, protocol: Optional[str] = None):
            self.protocol = protocol
            self.parts: List[CacheKeyPart] = []

        def set_protocol(self, value: str):
            self.protocol = value
            return self

        def add_string_part(self, value: str):
            self.parts.append(StringCacheKeyPart(value))
            return self

        def add_file_path_part(self, value: FilePath):
            self.parts.append(FilePathCacheKeyPart(value))
            return self

        def build(self) -> 'CacheKey':
            assert self.protocol is not None
            assert len(self.protocol) > 0
            assert len(self.parts) > 0
            string_parts = [self.protocol]
            for part in self.parts:
                string_parts.append(CacheKey.SEPARATOR)
                string_parts.append(part.get_string_part())
            string_key = "".join(string_parts)
            return CacheKey(self.protocol, self.parts, string_key)
