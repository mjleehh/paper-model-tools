class Model:
    def __init__(self, patches, connections, edges, vertices):
        self.patches = patches
        self.connections = connections
        self.edges = edges
        self.vertices = vertices


class ModelPatch:
    def __init__(self, parentConnectionSet, connectionSets):
        self.parentConnectionSet = parentConnectionSet
        self.connectionSets = connectionSets

    def __repr__(self):
        res = '('
        res += 'p = ' + repr(self.parentConnectionSet)
        res += ', c = ' + repr(self.connectionSets)
        res += ')'
        return res


class PatchConnection:
    def __init__(self, fstEdgeIndices, sndEdgeIndices=None):
        # index of first patch < index of second patch
        self._fstEdges = fstEdgeIndices
        self._sndEdges = sndEdgeIndices

    @property
    def isGlued(self):
        return self._sndEdges is not None

    def __repr__(self):
        res = '('
        if self.isGlued:
            res += 'E1 = ' + repr(self._fstEdges)
            res += ', E2 = ' + repr(self._sndEdges)
        else:
            res += 'E = ' + repr(self._fstEdges)
        res += ')'
        return res


class ModelEdge:
    def __init__(self, fstVertexIndex, sndVertexIndex):
        self.vertices = (fstVertexIndex, sndVertexIndex) if fstVertexIndex <= sndVertexIndex else (sndVertexIndex, fstVertexIndex)

    def __hash__(self):
        return hash(self.vertices)

    def __eq__(self, other):
        return self.vertices == other.vertices

    def __repr__(self):
        return repr(self.vertices)
