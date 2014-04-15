from unfolder.mesh.face_edge import FaceEdgeSubsetIter, FaceEdgeIter
from unfolder.mesh.mesh_impl import MeshImpl


class Face:
    def __init__(self, index, meshImpl: MeshImpl):
        self.meshImpl = meshImpl
        self.index = index

    def getConnectingEdges(self, otherFace):
        faceEdgeIndices = []
        for faceEdgeIndex, edgeIndex in enumerate(self.impl.edges):
            otherEdges = set(otherFace.impl.edges)
            if edgeIndex in otherEdges:
                faceEdgeIndices.append(faceEdgeIndex)
        return FaceEdgeSubsetIter(faceEdgeIndices, self.index, self.meshImpl)

    def getConnectedFaces(self):
        faceIndices = []
        edgeIndexSet = self.edges.indices
        for otherFaceIndex, otherFace in enumerate(self.meshImpl.faces):
            if otherFaceIndex != self.index:
                for otherFaceEdgeIndex in otherFace.edges:
                    if otherFaceEdgeIndex in edgeIndexSet:
                        faceIndices.append(otherFaceIndex)
        return FaceSubsetIter(faceIndices, self.meshImpl)

    def getNormal(self):
        e1 = self.edges[0].direction
        e2 = self.edges[1].direction
        return (e1 ^ e2).normalized()

    @property
    def vertices(self):
        vertexInds = self.vertexIndices
        for vertexIndex in vertexInds:
            yield self.meshImpl.vertices[vertexIndex]

    @property
    def vertexIndices(self):
        vertexIndices = []
        edges = [self.meshImpl.edges[edgeIndex].vertices for edgeIndex in self.impl.edges]
        prevEdge = edges[-1]
        for edge in edges:
            (fst, snd) = edge
            if fst in prevEdge:
                vertexIndices.append(fst)
            else:
                vertexIndices.append(snd)
            prevEdge = edge
        return vertexIndices

    @property
    def edges(self):
        return FaceEdgeIter(self.index, self.meshImpl)

    def __eq__(self, other):
        return self.index == other.index

    def __hash__(self):
        return hash(self.index)

    # private

    @property
    def impl(self):
        return self.meshImpl.faces[self.index]


# private


class FaceIter:
    def __init__(self, meshImpl: MeshImpl):
        self.meshImpl = meshImpl

    def __iter__(self):
        for faceIndex, val in enumerate(self.meshImpl.faces):
            yield self._item(faceIndex)

    def __len__(self):
        return len(self.meshImpl.faces)

    def __getitem__(self, faceIndex):
        return self._item(faceIndex)

    # private

    def _item(self, faceIndex):
        return Face(faceIndex, self.meshImpl)


class FaceSubsetIter:
    def __init__(self, indices, meshImpl: MeshImpl):
        self.indices = indices
        self.meshImpl = meshImpl

    def __iter__(self):
        for faceIndex in self.indices:
            yield self._item(faceIndex)

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, item):
        return self._item(self.indices[item])

    # private

    def _item(self, faceIndex):
        return Face(faceIndex, self.meshImpl)

