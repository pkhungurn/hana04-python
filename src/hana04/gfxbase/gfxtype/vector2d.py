from numbers import Number

import numpy

from hana04.gfxbase.gfxtype.tuple2 import Tuple2
from hana04.gfxbase.gfxtype.vector import Vector


class Vector2d(Tuple2, Vector):
    def __init__(self, *args, copy: bool = True):
        if len(args) == 0:
            self.data = numpy.zeros(2, dtype=numpy.float64)
        elif len(args) == 1:
            if isinstance(args[0], Tuple2):
                self.data = numpy.array([args[0].x, args[0].y], dtype=numpy.float64)
            else:
                assert isinstance(args[0], numpy.ndarray)
                assert args[0].dtype == numpy.float64
                assert args[0].shape == (2,)
                if copy:
                    self.data = numpy.copy(args[0])
                else:
                    self.data = args[0]
        elif len(args) == 2:
            self.data = numpy.array([float(args[0]), float(args[1])], dtype=numpy.float64)
        else:
            raise ValueError("Vector2d's constructor only accepts no arguments, a numpy.ndarray, or two numbers.")

    @property
    def x(self):
        return self.data[0]

    @property
    def y(self):
        return self.data[1]

    @property
    def u(self):
        return self.data[0]

    @property
    def v(self):
        return self.data[1]

    @property
    def s(self):
        return self.data[0]

    @property
    def t(self):
        return self.data[0]

    def __getitem__(self, item: int):
        return self.data[item]

    def __abs__(self):
        return Vector2d(numpy.abs(self.data), copy=False)

    def __add__(self, other):
        if isinstance(other, Vector2d):
            return Vector2d(self.data + other.data, copy=False)
        elif isinstance(other, Number):
            return Vector2d(self.data + numpy.float64(other), copy=False)
        else:
            raise ValueError(f"Cannot add a Vector2d to a {type(other)}")

    def __sub__(self, other):
        if isinstance(other, Vector2d):
            return Vector2d(self.data - other.data, copy=False)
        elif isinstance(other, Number):
            return Vector2d(self.data - numpy.float64(other), copy=False)
        else:
            raise ValueError(f"Cannot subtract a {type(other)} from a Vector2d")

    def __rsub__(self, other):
        if isinstance(other, Number):
            return Vector2d(numpy.float64(other) - self.data, copy=False)
        else:
            raise ValueError(f"Cannot subtract a {Vector2d} from a {type(other)}")

    def __mul__(self, scalar):
        if isinstance(scalar, Number) or isinstance(scalar, numpy.number):
            return Vector2d(self.data * numpy.float64(scalar), copy=False)
        else:
            raise ValueError(f"Cannot multiply a Vector2d to a {type(scalar)}")

    def __rmul__(self, scalar):
        if isinstance(scalar, Number) or isinstance(scalar, numpy.number):
            return Vector2d(self.data * numpy.float64(scalar), copy=False)
        else:
            raise ValueError(f"Cannot multiply a Vector2d to a {type(scalar)}")

    def __truediv__(self, scalar):
        if isinstance(scalar, Number) or isinstance(scalar, numpy.number):
            return Vector2d(self.data / numpy.float64(scalar), copy=False)
        else:
            raise ValueError(f"Cannot divide a Vector2d with a {type(scalar)}")

    def __rtruediv__(self, scalar):
        if isinstance(scalar, Number) or isinstance(scalar, numpy.number):
            return Vector2d(numpy.float64(scalar) / self.data, copy=False)
        else:
            raise ValueError(f"Cannot divide a Vector2d with a {type(scalar)}")

    def __eq__(self, other):
        if not isinstance(other, Vector2d):
            return False
        return numpy.array_equal(self.data, other.data)

    def __repr__(self):
        return f"Vector2d({self.x}, {self.y})"

    def length_squared(self):
        return numpy.sum(self.data ** 2)

    def length(self):
        return numpy.sqrt(self.length_squared())

    def normalized(self):
        return Vector2d(self.data / self.length)
