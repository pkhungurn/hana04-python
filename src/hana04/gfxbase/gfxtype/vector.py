from abc import ABC, abstractmethod


class Vector(ABC):
    @abstractmethod
    def __abs__(self):
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

    @abstractmethod
    def __rtruediv__(self, other):
        pass

    @abstractmethod
    def length_squared(self):
        pass

    @abstractmethod
    def length(self):
        pass

    @abstractmethod
    def normalized(self):
        pass