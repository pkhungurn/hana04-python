from abc import ABC, abstractmethod


class Tuple2(ABC):
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
    def u(self):
        pass

    @property
    @abstractmethod
    def v(self):
        pass

    @property
    @abstractmethod
    def s(self):
        pass

    @property
    @abstractmethod
    def t(self):
        pass

    @abstractmethod
    def __getitem__(self, item):
        pass