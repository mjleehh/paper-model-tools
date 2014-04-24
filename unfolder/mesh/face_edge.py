from unfolder.mesh.mesh_impl import MeshImpl
from unfolder.util.vector import Vector


class FaceEdge:
    def __init__(self, index, faceIndex, meshImpl: MeshImpl):
        self.index = index
        self.faceIndex = faceIndex
        self.meshImpl = meshImpl

    def __getitem__(self, item):
        vertexIndex = self._getEdgeVertices(self.index)[item]
        return self.meshImpl.vertices[vertexIndex]

    @property
    def direction(self):
        res = Vector(self.end) - Vector(self.begin)
        if res.norm() == 0:
            raise Exception('can not compute direction for 0 length edge')
        return res

    @property
    def begin(self):
        return self[1] if self._isFlipped() else self[0]

    @property
    def end(self):
        return self[0] if self._isFlipped() else self[1]

    def __eq__(self, other):
        return self.faceIndex == other.faceIndex and self.index == other.index

    def __hash__(self):
        return hash((self.index, self.faceIndex))

    # private

    def _isFlipped(self):
        prevEdge = self._getEdgeVertices(self.index - 1)
        (fst, snd) = self._getEdgeVertices(self.index)
        return fst in prevEdge

    def _getEdgeVertices(self, faceEdgeIndex):
        absoluteEdgeIndex = self.meshImpl.faces[self.faceIndex].edges[faceEdgeIndex]
        return self.meshImpl.edges[absoluteEdgeIndex].vertices


# private


class FaceEdgeIter:
    def __init__(self, faceIndex, meshImpl: MeshImpl):
        self.meshImpl = meshImpl
        self._faceIndex = faceIndex

    def __iter__(self):
        for faceEdgeIndex, val in enumerate(self.indices):
            yield self._item(faceEdgeIndex)

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, faceEdgeIndex):
        return self._item(faceEdgeIndex)

    @property
    def indices(self):
        return self.meshImpl.faces[self._faceIndex].edges

    def _item(self, faceEdgeIndex):
        return FaceEdge(faceEdgeIndex, self._faceIndex, self.meshImpl)


class FaceEdgeSubsetIter:
    def __init__(self, indices, faceIndex, meshImpl: MeshImpl):
        self.indices = indices
        self.faceIndex = faceIndex
        self.meshImpl = meshImpl

    def __iter__(self):
        for edgeIndex in self.indices:
            yield self._item(edgeIndex)

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, item):
        return self._item(self.indices[item])

    def _item(self, edgeIndex):
        return FaceEdge(edgeIndex, self.faceIndex, self.meshImpl)