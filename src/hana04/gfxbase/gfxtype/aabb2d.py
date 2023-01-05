import sys
from typing import Optional, Union

import numpy

from hana04.gfxbase.gfxtype.point2d import Point2d
from hana04.gfxbase.gfxtype.point2f import Point2f


class Aabb2d:
    def __init__(self, p_min: Optional[Point2d] = None, p_max: Optional[Point2d] = None):
        if p_min is None:
            p_min = Point2d(sys.float_info.max, sys.float_info.max)
        if p_max is None:
            p_max = Point2d(sys.float_info.min, sys.float_info.min)
        self.p_min = p_min
        self.p_max = p_max

    def is_valid(self):
        return numpy.all(numpy.less_equal(self.p_min.data, self.p_max.data))

    def expand_by(self, p: Union[Point2d, Point2f]):
        p_min = Point2d(numpy.minimum(self.p_min.data, p.data))
        p_max = Point2d(numpy.maximum(self.p_max.data, p.data))
        return Aabb2d(p_min, p_max)

    def __repr__(self):
        return f"Aabb2d(p_min = {self.p_min}, p_max = {self.p_max})"

    def __eq__(self, other):
        if not isinstance(other, Aabb2d):
            return False
        return self.p_min == other.p_min and self.p_max == other.p_max
