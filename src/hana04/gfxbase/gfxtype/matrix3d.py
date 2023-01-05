from numbers import Number

import numpy

from hana04.gfxbase.gfxtype.matrix3 import Matrix3
from hana04.gfxbase.gfxtype.matrix4 import Matrix4
from hana04.gfxbase.gfxtype.vector3f import Vector3f


class Matrix3d(Matrix3):
    def __init__(self, *args, copy: bool = True):
        if len(args) == 0:
            self.data = numpy.zeros((3, 3), dtype=numpy.float64)
        elif len(args) == 1:
            m = args[0]
            if isinstance(m, Matrix4):
                self.data = numpy.array(
                    [
                        [m[0, 0], m[0, 1], m[0, 2]],
                        [m[1, 0], m[1, 1], m[1, 2]],
                        [m[2, 0], m[2, 1], m[2, 2]]
                    ],
                    dtype=numpy.float64)
            elif isinstance(m, list):
                assert len(m) == 3
                assert isinstance(m[0], list) and isinstance(m[1], list) and isinstance(m[2], list)
                assert len(m[0]) == 3 and len(m[1]) == 3 and len(m[2]) == 3
                self.data = numpy.array(
                    [
                        [m[0][0], m[0][1], m[0][2]],
                        [m[1][0], m[1][1], m[1][2]],
                        [m[2][0], m[2][1], m[2][2]]
                    ],
                    dtype=numpy.float64)
            else:
                assert isinstance(m, numpy.ndarray)
                assert m.dtype == numpy.float64
                assert m.shape == (3, 3)
                if copy:
                    self.data = numpy.copy(m)
                else:
                    self.data = m
        elif len(args) == 3:
            m = args
            assert isinstance(m[0], list) and isinstance(m[1], list) and isinstance(m[2], list)
            self.data = numpy.array(
                [
                    [m[0][0], m[0][1], m[0][2]],
                    [m[1][0], m[1][1], m[1][2]],
                    [m[2][0], m[2][1], m[2][2]]
                ],
                dtype=numpy.float64)
        elif len(args) == 9:
            m = args
            self.data = numpy.array(
                [
                    [m[0], m[1], m[2]],
                    [m[3], m[4], m[5]],
                    [m[6], m[7], m[8]],
                ],
                dtype=numpy.float64)
        else:
            raise ValueError("Invalid Matrix3d constructor arguments.")

    def __getitem__(self, item):
        assert isinstance(item, tuple)
        assert len(item) == 2
        return self.data[item[0], item[1]]

    def __add__(self, other):
        if isinstance(other, Matrix3d):
            return Matrix3d(self.data + other.data, copy=False)
        elif isinstance(other, Number) or isinstance(other, numpy.number):
            return Matrix3d(self.data + numpy.float64(other), copy=False)
        else:
            raise ValueError(f"Cannot add a Matrix4d to a {type(other)}.")

    def __sub__(self, other):
        if isinstance(other, Matrix3d):
            return Matrix3d(self.data - other.data, copy=False)
        elif isinstance(other, Number) or isinstance(other, numpy.number):
            return Matrix3d(self.data - numpy.float64(other), copy=False)
        else:
            raise ValueError(f"Cannot subtract a {type(other)} from a Matrix4d.")

    def __rsub__(self, other):
        if isinstance(other, Number) or isinstance(other, numpy.number):
            return Matrix3d(numpy.float64(other) - self.data, copy=False)
        else:
            raise ValueError(f"Cannot subract a Matrix4d from a {type(other)}.")

    def __mul__(self, other):
        if isinstance(other, Matrix3d):
            return Matrix3d(numpy.matmul(self.data, other.data), copy=False)
        elif isinstance(other, Number) or isinstance(other, numpy.number):
            return Matrix3d(self.data * numpy.float64(other), copy=False)
        elif isinstance(other, Vector3f):
            return Vector3f((self.data * other.data.view((3, 1))).view(3, ), copy=False)
        else:
            raise ValueError(f"Cannot multiply a Matrix4d with a a {type(other)}.")

    def __rmul__(self, other):
        if isinstance(other, Number) or isinstance(other, numpy.number):
            return Matrix3d(self.data * numpy.float64(other), copy=False)
        else:
            raise ValueError(f"Cannot multiply a Matrix4d with a a {type(other)}.")

    def __truediv__(self, other):
        if isinstance(other, Number) or isinstance(other, numpy.number):
            return Matrix3d(self.data / numpy.float64(other), copy=False)
        else:
            raise ValueError(f"Cannot divide a Matrix4d with a a {type(other)}.")

    def __eq__(self, other):
        if not isinstance(other, Matrix3d):
            return False
        return numpy.array_equal(self.data, other.data)

    def __repr__(self):
        return f"Matrix3d([" \
               f"[{self.data[0, 0]}, {self.data[0, 1]}, {self.data[0, 2]}], " \
               f"[{self.data[1, 0]}, {self.data[1, 1]}, {self.data[1, 2]}], " \
               f"[{self.data[2, 0]}, {self.data[2, 1]}, {self.data[2, 2]}]])"


if __name__ == "__main__":
    m0 = Matrix3d(1, 0, 0, 0, 1, 0, 0, 0, 1)
    m1 = Matrix3d(2, 0, 0, 0, 4, 0, 0, 0, 8)
    print(m0 * m1)
    print(2 * m0)
    print(m0 / 2)
    print(type(m1[0, 0]))
    print(1 - m1)
