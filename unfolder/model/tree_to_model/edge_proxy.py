from unfolder.util.vector import Vector


class PatchEdgeProxy():
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    @property
    def direction(self):
        return Vector(self.end) - Vector(self.begin)
