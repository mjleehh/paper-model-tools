import maya.OpenMaya as om


class CoordinateSystem:
    """ A 2D coordinate system with origin other than 0 in 3D space

    origin   the origin of the coordinate system realtive to global space
    e1, e2   orthogonal unit vectors
    """
    def __init__(self, origin, e1, e2):
        self.origin = origin
        self.e1 = e1
        self.e2 = e2

    def toLocal(self, vg):
        vLocalOrigin = vg - self.origin
        return (self.e1 * vLocalOrigin, self.e2 * vLocalOrigin)

    def toGlobal(self, vl):
        fst = om.MVector(self.e1)
        fst *= vl[0]
        snd = om.MVector(self.e2)
        snd *= vl[1]
        trd = om.MVector(self.origin)
        vLocalOrigin = fst + snd
        return vLocalOrigin + trd