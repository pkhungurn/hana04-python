import numpy

from hana04.gfxbase.gfxtype.point import Point
from hana04.gfxbase.gfxtype.tuple2 import Tuple2


class Point2d(Tuple2, Point):
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
            raise ValueError("Point2d's constructor only accepts no arguments, a numpy.ndarray, or two numbers.")

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

    def __add__(self, other):
        from hana04.gfxbase.gfxtype.vector2f import Vector2f

        if isinstance(other, Vector2f):
            return Point2d(self.data + other.data, copy=False)
        else:
            raise ValueError(f"Cannot add a Point2d to a {type(other)}")

    def __sub__(self, other):
        from hana04.gfxbase.gfxtype.vector2f import Vector2f

        if isinstance(other, Point2d):
            return Vector2f(self.data - other.data, copy=False)
        elif isinstance(other, Vector2f):
            return Point2d(self.data - other.data, copy=False)
        else:
            raise ValueError(f"Cannot subtract a {type(other)} from a Point2d")

    def __eq__(self, other):
        if not isinstance(other, Point2d):
            return False
        return numpy.array_equal(self.data, other.data)

    def __repr__(self):
        return f"Point2d({self.x}, {self.y})"

    @staticmethod
    def distance_squared(a: 'Point2d', b: 'Point2d'):
        return numpy.sum((a.data - b.data) ** 2)

    @staticmethod
    def distance(a: 'Point2d', b: 'Point2d'):
        return numpy.sqrt(Point2d.distance_squared(a, b))


if __name__ == "__main__":
    v = Point2d(1, 2)
