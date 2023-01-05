from typing import Optional

from hana04.gfxbase.gfxtype.matrix4d import Matrix4d


class Transform:
    def __init__(self, m: Optional[Matrix4d] = None, mi: Optional[Matrix4d] = None, mit: Optional[Matrix4d] = None):
        if m is None:
            m = Matrix4d([
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ])
        if mi is None:
            mi = m.inverse()
        if mit is None:
            mit = mi.transpose()
        self.m = m
        self.mi = mi
        self.mit = mit

    def __repr__(self):
        return f"Transform({self.m})"

    def inverse(self):
        return Transform(m=Matrix4d(self.mi), mi=Matrix4d(self.m))

    @staticmethod
    def identity():
        return Transform()
