from unfolder.mesh.obj_mesh_impl import ObjMesh
from unfolder.util.vector import Vector

class Mesh:
    def __init__(self, objMesh: ObjMesh):
        self._objMesh= objMesh

    @property
    def faces(self):
        return MeshFaces(self._objMesh)

    @property
    def edges(self):
        return MeshEdges(self._objMesh)

    @property
    def vertices(self):
        return self._objMesh.vertices


class MeshFace:
    def __init__(self, objMesh: ObjMesh, index):
        self._objMesh = objMesh
        self.index = index

    def getConnectingEdges(self, otherFace):
        edges = set(self._value.edges)
        otherEdges = set(otherFace._value.edges)
        return [MeshEdge(edge, self._objMesh) for edge in edges & otherEdges]

    def getConnectedFaces(self):
        face = self._objMesh.faces[self.index]
        return [MeshFace(self._objMesh, faceIndex) for edge in face.edges for faceIndex in self._objMesh.edges[edge].faces if faceIndex != self.index]

    def getNormal(self):
        e1 = self.edges[0].direction
        e2 = self.edges[1].direction
        return (e1 ^ e2).normalized()

    @property
    def vertices(self):
        vertexInds = self.vertexIndices
        for vertexIndex in vertexInds:
            yield self._objMesh.vertices[vertexIndex]

    @property
    def vertexIndices(self):
        vertexIndices = []
        edges = [self._objMesh.edges[edgeIndex].vertices for edgeIndex in self._value.edges]
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
        return MeshFaceEdges(self.index, self._objMesh)

    @property
    def edgeIndices(self):
        return self._value.edges

    def __eq__(self, other):
        return self.index == other.index

    def __hash__(self):
        return hash(self.index)

    # private

    @property
    def _value(self):
        return self._objMesh.faces[self.index]


class MeshFaceEdges:
    def __init__(self, faceIndex, objMesh: ObjMesh):
        self._objMesh = objMesh
        self._faceIndex = faceIndex

    def __getitem__(self, item):
        prevEdge = self._getEdgeVertices(item - 1)
        (fst, snd) = self._getEdgeVertices(item)
        edgeIndex = self._edgeIndices[item]
        flipped = fst in prevEdge
        return MeshEdge(edgeIndex, self._objMesh, flipped)

    def __len__(self):
        return len(self._edgeIndices)

    def __iter__(self):
        for faceEdgeIndex, val in enumerate(self._edgeIndices):
            yield self[faceEdgeIndex]

    # private

    def _getEdgeVertices(self, index):
        edgeIndex = self._edgeIndices[index]
        return self._objMesh.edges[edgeIndex].vertices

    @property
    def _edgeIndices(self):
        return self._objMesh.faces[self._faceIndex].edges


class MeshEdge:
    def __init__(self, index, objMesh: ObjMesh, flipped=False):
        self._objMesh = objMesh
        self.index = index
        self.flipped = flipped

    def __getitem__(self, item):
        return self._objMesh.vertices[self._value.vertices[item]]

    @property
    def direction(self):
        return Vector(self.end) - Vector(self.begin)

    @property
    def begin(self):
        return self[0] if not self.flipped else self[1]

    @property
    def end(self):
        return self[1] if not self.flipped else self[0]

    def __eq__(self, other):
        return self.index == other.index

    def __hash__(self):
        return hash(self.index)

    # private

    @property
    def _value(self):
        return self._objMesh.edges[self.index]


# private


class MeshFaces:
    def __init__(self, objMesh: ObjMesh):
        self._objMesh = objMesh

    def __len__(self):
        return len(self._objMesh.faces)

    def __getitem__(self, faceIndex):
        return MeshFace(self._objMesh, faceIndex)

    def __iter__(self):
        for faceIndex, val in enumerate(self._objMesh.faces):
            yield self[faceIndex]


class MeshEdges:
    def __init__(self, objMesh: ObjMesh):
        self._objMesh = objMesh

    def __len__(self):
        return len(self._objMesh.edges)

    def __getitem__(self, edgeIndex):
        return MeshEdge(edgeIndex, self._objMesh)

    def __iter__(self):
        for edgeIndex, val in enumerate(self._objMesh.edges):
            yield self[edgeIndex]
