from abc import ABC, abstractmethod


class Tuple3(ABC):
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
    def u(self):
        pass

    @property
    @abstractmethod
    def v(self):
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

    @abstractmethod
    def __getitem__(self, item):
        pass