from copy import copy
import numpy as np
import numpy.linalg as lg


class Vector:
    def __init__(self, *v):
        if len(v) < 1:
            raise DimensionError('Vector must have finite dimension!')
        if len(v) == 1:
            self.v = np.array(v[0])
        else:
            self.v = np.array(v)

    def __add__(self, other):
        if not self._hasSameDim(other):
            raise DimensionError('Can not sum vectors with different dimensions!')
        return Vector(self.v + other.v) if isVector(other) else Vector(self.v + other)

    def __sub__(self, other):
        if not self._hasSameDim(other):
            raise DimensionError('Can not subtract vectors with different dimensions!')
        return Vector(self.v - other.v) if isVector(other) else Vector(self.v - other)

    def __mul__(self, other):
        # works for vectors and scalars
        res = np.dot(self.v, other)
        return res if not isinstance(res, np.ndarray) else Vector(res)

    def __truediv__(self, scalar):
        if not isinstance(scalar, (int, float, complex)):
            raise DimensionError('Divisor must be scalar!')
        v = self.v.astype(float)
        if scalar == 0:
            raise Exception('Cannot rescale vector by divisor 0')
        v /= scalar
        return Vector(v)

    def __xor__(self, other):
        if not self._hasSameDim(other):
            raise DimensionError('Can not cross multiply vectors with different dimensions')
        return Vector(np.cross(self.v, other))

    def norm(self):
        return lg.norm(self.v)

    def normalized(self):
        return self / self.norm()

    def __len__(self):
        return self.v.size

    def __getitem__(self, item):
        return self.v[item]

    def __iter__(self):
        for item in self.v:
            yield item

    def __eq__(self, other):
        if len(self.v) != len(other):
            raise DimensionError('Can not compare two vectors of different dimension')
        for index, item in enumerate(self):
            if item != other[index]:
                return False
        return True

    def __repr__(self):
        res = '('
        delim = ''
        for coord in self.v:
            res += delim
            res += repr(coord)
            delim = ', '
        res += ')'
        return res

    # private

    def _hasSameDim(self, v):
        return len(self) == len(v)

def isVector(x):
    return isinstance(x, Vector)

class DimensionError(Exception):
    def __init__(self, msg):
        super(msg)