from abc import ABC, abstractmethod


class Tuple4(ABC):
    @property
    @abstractmethod
    def x(self):
        pass

    @property
    @abstractmethod
    def y(self):
        pass

    @property
    @abstractmethod
    def z(self):
        pass

    @property
    @abstractmethod
    def w(self):
        pass

    @property
    @abstractmethod
    def r(self):
        pass

    @property
    @abstractmethod
    def g(self):
        pass

    @property
    @abstractmethod
    def b(self):
        pass

    @property
    @abstractmethod
    def a(self):
        pass
