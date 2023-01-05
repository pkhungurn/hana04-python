import math
from numbers import Number

import numpy
import quaternion

from hana04.gfxbase.gfxtype.tuple4 import Tuple4


class Quat4d:
    def __init__(self, *args, copy: bool = True):
        if len(args) == 0:
            self.data = numpy.quaternion(1.0, 0.0, 0.0, 0.0)
        elif len(args) == 1:
            if isinstance(args[0], Tuple4):
                self.data = numpy.quaternion([args[0].w, args[0].x, args[0].y, args[0].z])
            else:
                assert isinstance(args[0], numpy.quaternion)
                if copy:
                    self.data = numpy.copy(args[0])
                else:
                    self.data = args[0]
        elif len(args) == 4:
            self.data = numpy.quaternion(
                float(args[0]), float(args[1]), float(args[2]), float(args[3]))
        else:
            raise ValueError("Quat4d's constructor only accepts no arguments, a numpy.quaternion, or four numbers.")

    @property
    def x(self):
        return self.data.x

    @property
    def y(self):
        return self.data.y

    @property
    def z(self):
        return self.data.z

    @property
    def w(self):
        return self.data.w

    def __getitem__(self, item: int):
        return self.data[item]

    def __repr__(self):
        return f"Quat4d({self.w}; {self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        if isinstance(other, Quat4d):
            return Quat4d(self.data + other.data, copy=False)
        elif isinstance(other, Number):
            return Quat4d(self.data + numpy.float64(other), copy=False)
        else:
            raise ValueError(f"Cannot add a Quat4d to a {type(other)}")

    def __sub__(self, other):
        if isinstance(other, Quat4d):
            return Quat4d(self.data - other.data, copy=False)
        elif isinstance(other, Number) or isinstance(other, numpy.number):
            return Quat4d(self.data - numpy.float64(other), copy=False)
        else:
            raise ValueError(f"Cannot subtract a {type(other)} from a Quat4d")

    def __rsub__(self, other):
        if isinstance(other, Number) or isinstance(other, numpy.number):
            return Quat4d(numpy.float64(other) - self.data, copy=False)
        else:
            raise ValueError(f"Cannot subtract a {Quat4d} from a {type(other)}")

    def __mul__(self, other):
        if isinstance(other, Number) or isinstance(other, numpy.number):
            return Quat4d(self.data * numpy.float64(other), copy=False)
        elif isinstance(other, Quat4d):
            return Quat4d(self.data * other.data, copy=False)
        else:
            raise ValueError(f"Cannot multiply a Quat4d to a {type(other)}")

    def __rmul__(self, scalar):
        if isinstance(scalar, Number) or isinstance(scalar, numpy.number):
            return Quat4d(self.data * numpy.float64(scalar), copy=False)
        else:
            raise ValueError(f"Cannot multiply a Quat4d to a {type(scalar)}")

    def __truediv__(self, scalar):
        if isinstance(scalar, Number) or isinstance(scalar, numpy.number):
            return Quat4d(self.data / numpy.float64(scalar), copy=False)
        else:
            raise ValueError(f"Cannot divide a Quat4d with a {type(scalar)}")

    def __rtruediv__(self, scalar):
        if isinstance(scalar, Number) or isinstance(scalar, numpy.number):
            return Quat4d(numpy.float64(scalar) / self.data, copy=False)
        else:
            raise ValueError(f"Cannot divide a Vector4d with a {type(scalar)}")

    def __eq__(self, other):
        if not isinstance(other, Quat4d):
            return False
        return self.data == other.data

    def length_squared(self):
        return numpy.sum(quaternion.as_float_array(self.data) ** 2)

    def length(self):
        return numpy.sqrt(self.length_squared())

    def normalized(self):
        return Quat4d(self.data / self.length())


if __name__ == "__main__":
    q0 = Quat4d()
    theta = math.pi / 3
    c = math.cos(theta / 2)
    s = math.sin(theta / 2)
    q1 = Quat4d(c, -s, 0, 0)
    print(q1)
    print(q1.data ** 2)
    print(q1.length_squared())