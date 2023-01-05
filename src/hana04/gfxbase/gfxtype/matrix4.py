from abc import ABC, abstractmethod


class Matrix4(ABC):
    @abstractmethod
    def __getitem__(self, item):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __sub__(self, other):
        pass

    @abstractmethod
    def __rsub__(self, other):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __rmul__(self, other):
        pass

    @abstractmethod
    def __truediv__(self, other):
        pass
