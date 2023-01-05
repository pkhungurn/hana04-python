import sys
from typing import Optional, Union

import numpy

from hana04.gfxbase.gfxtype.point3d import Point3d
from hana04.gfxbase.gfxtype.point3f import Point3f


class Aabb3d:
    def __init__(self, p_min: Optional[Point3d] = None, p_max: Optional[Point3d] = None):
        if p_min is None:
            p_min = Point3d(sys.float_info.max, sys.float_info.max, sys.float_info.max)
        if p_max is None:
            p_max = Point3d(sys.float_info.min, sys.float_info.min, sys.float_info.min)
        self.p_max = p_max
        self.p_min = p_min

    def is_valid(self):
        return numpy.all(numpy.less_equal(self.p_min.data, self.p_max.data))

    def expand_by(self, p: Union[Point3d, Point3f]):
        p_min = Point3d(numpy.minimum(self.p_min.data, p.data))
        p_max = Point3d(numpy.maximum(self.p_max.data, p.data))
        return Aabb3d(p_min, p_max)

    def __repr__(self):
        return f"Aabb3d(p_min = {self.p_min}, p_max = {self.p_max})"

    def __eq__(self, other):
        if not isinstance(other, Aabb3d):
            return False
        return self.p_min == other.p_min and self.p_max == other.p_max


if __name__ == "__main__":
    aabb = Aabb3d()
    print(aabb.is_valid())
