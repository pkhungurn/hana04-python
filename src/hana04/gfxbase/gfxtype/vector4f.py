from numbers import Number

import numpy

from hana04.gfxbase.gfxtype.tuple4 import Tuple4
from hana04.gfxbase.gfxtype.vector import Vector


class Vector4f(Tuple4, Vector):
    def __init__(self, *args, copy: bool = True):
        if len(args) == 0:
            self.data = numpy.zeros(4, dtype=numpy.float32)
        elif len(args) == 1:
            if isinstance(args[0], Tuple4):
                self.data = numpy.array([args[0].x, args[0].y, args[0].z, args[0].w], dtype=numpy.float32)
            else:
                assert isinstance(args[0], numpy.ndarray)
                assert args[0].dtype == numpy.float32
                assert args[0].shape == (4,)
                if copy:
                    self.data = numpy.copy(args[0])
                else:
                    self.data = args[0]
        elif len(args) == 4:
            self.data = numpy.array(
                [float(args[0]), float(args[1]), float(args[2]), float(args[3])],
                dtype=numpy.float32)
        else:
            raise ValueError("Vector4f's constructor only accepts no arguments, a numpy.ndarray, or four numbers.")

    @property
    def x(self):
        return self.data[0]

    @property
    def y(self):
        return self.data[1]

    @property
    def z(self):
        return self.data[2]

    @property
    def w(self):
        return self.data[3]

    @property
    def r(self):
        return self.data[0]

    @property
    def g(self):
        return self.data[1]

    @property
    def b(self):
        return self.data[2]

    @property
    def a(self):
        return self.data[3]

    def __getitem__(self, item: int):
        return self.data[item]

    def __abs__(self):
        return Vector4f(numpy.abs(self.data), copy=False)

    def __add__(self, other):
        if isinstance(other, Vector4f):
            return Vector4f(self.data + other.data, copy=False)
        elif isinstance(other, Number):
            return Vector4f(self.data + numpy.float32(other), copy=False)
        else:
            raise ValueError(f"Cannot add a Vector4f to a {type(other)}")

    def __sub__(self, other):
        if isinstance(other, Vector4f):
            return Vector4f(self.data - other.data, copy=False)
        elif isinstance(other, Number):
            return Vector4f(self.data - numpy.float32(other), copy=False)
        else:
            raise ValueError(f"Cannot subtract a {type(other)} from a Vector4f")

    def __rsub__(self, other):
        if isinstance(other, Number):
            return Vector4f(numpy.float32(other) - self.data, copy=False)
        else:
            raise ValueError(f"Cannot subtract a {Vector4f} from a {type(other)}")

    def __mul__(self, scalar):
        if isinstance(scalar, Number) or isinstance(scalar, numpy.number):
            return Vector4f(self.data * numpy.float32(scalar), copy=False)
        else:
            raise ValueError(f"Cannot multiply a Vector4f to a {type(scalar)}")

    def __rmul__(self, scalar):
        if isinstance(scalar, Number) or isinstance(scalar, numpy.number):
            return Vector4f(self.data * numpy.float32(scalar), copy=False)
        else:
            raise ValueError(f"Cannot multiply a Vector4f to a {type(scalar)}")

    def __truediv__(self, scalar):
        if isinstance(scalar, Number) or isinstance(scalar, numpy.number):
            return Vector4f(self.data / numpy.float32(scalar), copy=False)
        else:
            raise ValueError(f"Cannot divide a Vector4f with a {type(scalar)}")

    def __rtruediv__(self, scalar):
        if isinstance(scalar, Number) or isinstance(scalar, numpy.number):
            return Vector4f(numpy.float32(scalar) / self.data, copy=False)
        else:
            raise ValueError(f"Cannot divide a Vector4f with a {type(scalar)}")

    def __eq__(self, other):
        if not isinstance(other, Vector4f):
            return False
        return numpy.array_equal(self.data, other.data)

    def __repr__(self):
        return f"Vector4f({self.x}, {self.y}, {self.z}, {self.w})"

    def length_squared(self):
        return numpy.sum(self.data ** 2)

    def length(self):
        return numpy.sqrt(self.length_squared())

    def normalized(self):
        return Vector4f(self.data / self.length)
