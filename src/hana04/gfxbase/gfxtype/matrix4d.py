from numbers import Number

import numpy

from hana04.gfxbase.gfxtype.matrix4 import Matrix4
from hana04.gfxbase.gfxtype.vector4d import Vector4d


class Matrix4d(Matrix4):
    def __init__(self, *args, copy: bool = True):
        if len(args) == 0:
            self.data = numpy.zeros((4, 4), dtype=numpy.float64)
        elif len(args) == 1:
            m = args[0]
            if isinstance(m, Matrix4):
                self.data = numpy.array(
                    [
                        [m[0, 0], m[0, 1], m[0, 2], m[0, 3]],
                        [m[1, 0], m[1, 1], m[1, 2], m[1, 3]],
                        [m[2, 0], m[2, 1], m[2, 2], m[2, 3]],
                        [m[3, 0], m[3, 1], m[3, 2], m[3, 3]],
                    ],
                    dtype=numpy.float64)
            elif isinstance(m, list):
                assert len(m) == 4
                assert isinstance(m[0], list) \
                       and isinstance(m[1], list) \
                       and isinstance(m[2], list) \
                       and isinstance(m[3], list)
                assert len(m[0]) == 4 \
                       and len(m[1]) == 4 \
                       and len(m[2]) == 4 \
                       and len(m[3]) == 4
                self.data = numpy.array(
                    [
                        [m[0][0], m[0][1], m[0][2], m[0][3]],
                        [m[1][0], m[1][1], m[1][2], m[1][3]],
                        [m[2][0], m[2][1], m[2][2], m[2][3]],
                        [m[3][0], m[3][1], m[3][2], m[3][3]]
                    ],
                    dtype=numpy.float64)
            else:
                assert isinstance(m, numpy.ndarray)
                assert m.dtype == numpy.float64
                assert m.shape == (4, 4)
                if copy:
                    self.data = numpy.copy(m)
                else:
                    self.data = m
        elif len(args) == 4:
            m = args
            assert isinstance(m[0], list) \
                   and isinstance(m[1], list) \
                   and isinstance(m[2], list) \
                   and isinstance(m[3], list)
            assert len(m[0]) == 4 \
                   and len(m[1]) == 4 \
                   and len(m[2]) == 4 \
                   and len(m[3]) == 4
            self.data = numpy.array(
                [
                    [m[0][0], m[0][1], m[0][2], m[0][3]],
                    [m[1][0], m[1][1], m[1][2], m[1][3]],
                    [m[2][0], m[2][1], m[2][2], m[2][3]],
                    [m[3][0], m[3][1], m[3][2], m[3][3]],
                ],
                dtype=numpy.float64)
        elif len(args) == 16:
            m = args
            self.data = numpy.array(
                [
                    [m[0], m[1], m[2], m[3]],
                    [m[4], m[5], m[6], m[7]],
                    [m[8], m[9], m[10], m[11]],
                    [m[12], m[13], m[14], m[15]],
                ],
                dtype=numpy.float64)
        else:
            raise ValueError("Invalid Matrix4d constructor arguments.")

    def __getitem__(self, item):
        assert isinstance(item, tuple)
        assert len(item) == 2
        return self.data[item[0], item[1]]

    def __add__(self, other):
        if isinstance(other, Matrix4d):
            return Matrix4d(self.data + other.data, copy=False)
        elif isinstance(other, Number) or isinstance(other, numpy.number):
            return Matrix4d(self.data + numpy.float64(other), copy=False)
        else:
            raise ValueError(f"Cannot add a Matrix4d to a {type(other)}.")

    def __sub__(self, other):
        if isinstance(other, Matrix4d):
            return Matrix4d(self.data - other.data, copy=False)
        elif isinstance(other, Number) or isinstance(other, numpy.number):
            return Matrix4d(self.data - numpy.float64(other), copy=False)
        else:
            raise ValueError(f"Cannot subtract a {type(other)} from a Matrix4d.")

    def __rsub__(self, other):
        if isinstance(other, Number) or isinstance(other, numpy.number):
            return Matrix4d(numpy.float64(other) - self.data, copy=False)
        else:
            raise ValueError(f"Cannot subract a Matrix4d from a {type(other)}.")

    def __mul__(self, other):
        if isinstance(other, Matrix4d):
            return Matrix4d(numpy.matmul(self.data, other.data), copy=False)
        elif isinstance(other, Number) or isinstance(other, numpy.number):
            return Matrix4d(self.data * numpy.float64(other), copy=False)
        elif isinstance(other, Vector4d):
            return Vector4d((self.data * other.data.view((4, 1))).view(4, ), copy=False)
        else:
            raise ValueError(f"Cannot multiply a Matrix4d with a a {type(other)}.")

    def __rmul__(self, other):
        if isinstance(other, Number) or isinstance(other, numpy.number):
            return Matrix4d(self.data * numpy.float64(other), copy=False)
        else:
            raise ValueError(f"Cannot multiply a Matrix4d with a a {type(other)}.")

    def __truediv__(self, other):
        if isinstance(other, Number) or isinstance(other, numpy.number):
            return Matrix4d(self.data / numpy.float64(other), copy=False)
        else:
            raise ValueError(f"Cannot divide a Matrix4d with a a {type(other)}.")

    def __eq__(self, other):
        if not isinstance(other, Matrix4d):
            return False
        return numpy.array_equal(self.data, other.data)

    def __repr__(self):
        return f"Matrix4d([" \
               f"[{self.data[0, 0]}, {self.data[0, 1]}, {self.data[0, 2]}, {self.data[0, 3]}], " \
               f"[{self.data[1, 0]}, {self.data[1, 1]}, {self.data[1, 2]}, {self.data[1, 3]}], " \
               f"[{self.data[2, 0]}, {self.data[2, 1]}, {self.data[2, 2]}, {self.data[2, 3]}], " \
               f"[{self.data[3, 0]}, {self.data[3, 1]}, {self.data[3, 2]}, {self.data[3, 3]}], " \
               f"])"

    def inverse(self):
        return Matrix4d(numpy.linalg.inv(self.data), copy=False)

    def transpose(self):
        return Matrix4d(numpy.transpose(self.data), copy=False)


if __name__ == "__main__":
    m0 = Matrix4d([1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1])
    m1 = Matrix4d([2, 0, 0, 0], [0, 4, 0, 0], [0, 0, 8, 0], [0, 0, 0, 1])
    print(m0 * m1)
    print(2 * m0)
    print(m0 / 2)
    print(m1[0, 0])
    print(1 - m1)
