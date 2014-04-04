import numpy as np
import numpy.linalg as lg

class Vector:
    def __init__(self, *v):
        if len(v) == 1:
            self.v = np.array(v[0])
        else:
            self.v = np.array(v)

    def __add__(self, other):
        self.v + other

    def __sub__(self, other):
        self.v - other

    def __mul__(self, other):
        # works for vectors and scalars
        np.dot(self.v, other)

    def __pow__(self, other, modulo=None):
        return np.cross(self.v, other)

    def norm(self):
        return lg.norm(self.v)

    def normalize(self):
        self.v /= self.norm()

    def __getitem__(self, item):
        return self.v[item]

    def __repr__(self):
        res = '('
        delim = ''
        for coord in self.v:
            res += delim
            res += repr(coord)
            delim = ', '
        res += ')'
        return res

