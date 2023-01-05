import numpy

from hana04.gfxbase.gfxtype.point import Point
from hana04.gfxbase.gfxtype.tuple3 import Tuple3


class Point3f(Tuple3, Point):
    def __init__(self, *args, copy: bool = True):
        if len(args) == 0:
            self.data = numpy.zeros(3, dtype=numpy.float32)
        elif len(args) == 1:
            if isinstance(args[0], Tuple3):
                self.data = numpy.array([args[0].x, args[0].y, args[0].z], dtype=numpy.float32)
            else:
                assert isinstance(args[0], numpy.ndarray)
                assert args[0].dtype == numpy.float32
                assert args[0].shape == (3,)
                if not copy:
                    self.data = args[0]
                else:
                    self.data = numpy.copy(args[0])
        elif len(args) == 3:
            self.data = numpy.array([float(args[0]), float(args[1]), float(args[2])], dtype=numpy.float32)
        else:
            raise ValueError("Point3f's constructor only accepts no arguments, a numpy.ndarray, or three numbers.")

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
    def u(self):
        return self.data[0]

    @property
    def v(self):
        return self.data[1]

    @property
    def w(self):
        return self.data[2]

    @property
    def r(self):
        return self.data[0]

    @property
    def g(self):
        return self.data[1]

    @property
    def b(self):
        return self.data[2]

    def __getitem__(self, item: int):
        return self.data[item]

    def __add__(self, other):
        from hana04.gfxbase.gfxtype.vector3f import Vector3f

        if isinstance(other, Vector3f):
            return Point3f(self.data + other.data, copy=False)
        else:
            raise ValueError(f"Cannot add a Point3f to a {type(other)}")

    def __sub__(self, other):
        from hana04.gfxbase.gfxtype.vector3f import Vector3f

        if isinstance(other, Point3f):
            return Vector3f(self.data - other.data, copy=False)
        elif isinstance(other, Vector3f):
            return Point3f(self.data - other.data, copy=False)
        else:
            raise ValueError(f"Cannot subtract a {type(other)} from a Point3f")

    def __eq__(self, other):
        if not isinstance(other, Point3f):
            return False
        return numpy.array_equal(self.data, other.data)

    def __repr__(self):
        return f"Point3f({self.x}, {self.y}, {self.z})"

    @staticmethod
    def distance_squared(a: 'Point3f', b: 'Point3f'):
        return numpy.sum((a.data - b.data) ** 2)

    @staticmethod
    def distance(a: 'Point3f', b: 'Point3f'):
        return numpy.sqrt(Point3f.distance_squared(a, b))