from unfolder.util.vector import Vector


class PlaneCoordinateSystem:
    """ A 2D coordinate system with origin other than 0 in 3D space

    origin   the origin of the coordinate system realtive to global space
    e1, e2   orthogonal unit vectors
    """
    def __init__(self, origin, e1, e2):
        self.origin = Vector(origin)
        self.e1 = Vector(e1)
        self.e2 = Vector(e2)

    def toLocal(self, vg):
        vLocalOrigin = Vector(vg) - self.origin
        return self.e1 * vLocalOrigin, self.e2 * vLocalOrigin

    def toGlobal(self, vl):
        fst = self.e1
        fst *= vl[0]
        snd = self.e2
        snd *= vl[1]
        trd = self.origin
        vLocalOrigin = fst + snd
        return vLocalOrigin + trd