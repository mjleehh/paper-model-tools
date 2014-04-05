from unfolder.util.vector import Vector


class MeshFaces:
    def __init__(self, objMesh):
        self._objMesh = objMesh

    def __len__(self):
        return len(self._objMesh.faces)

    def __getitem__(self, faceIndex):
        return MeshFace(self._objMesh, faceIndex)

    def __contains__(self, faceIndex):
        return 0 <= faceIndex < len(self._objMesh.faces)

    def __iter__(self):
        for faceIndex in range(len(self._objMesh.faces)):
            yield self[faceIndex]


class MeshFace:
    def __init__(self, objMesh, index):
        self._objMesh = objMesh
        self.index = index

    def getConnectingEdges(self, otherFace):
        edges = set(self._value.edges)
        otherEdges = set(otherFace._value.edges)
        return edges & otherEdges

    def getConnectedFaces(self):
        face = self._objMesh.faces[self.index]
        return [MeshFace(self._objMesh, faceIndex) for edge in face.edges for faceIndex in self._objMesh.edges[edge].faces if faceIndex != self.index]

    def getNormal(self):
        vertices1 = self.edgeIndices[0]
        vertices2 = self.edgeIndices[1]
        v2 = vertices1 & vertices2
        v1 = vertices1 - v2
        v3 = vertices2 - v2
        e1 = Vector(v2) - Vector(v1)
        e2 = Vector(v3) - Vector(v2)
        print(e1 ^ e2)

    @property
    def vertices(self):
        vertexInds = self._getVertexIndices()
        for vertexIndex in vertexInds:
            yield self._objMesh.vertices[vertexIndex]

    @property
    def edges(self):
        return MeshFaceEdges(self.index, self._objMesh)

    @property
    def edgeIndices(self):
        return self._value.edges

    # private

    def _getVertexIndices(self):
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
    def _value(self):
        return self._objMesh.faces[self.index]


class MeshFaceEdges:
    def __init__(self, faceIndex, objMesh):
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
        for faceEdgeIndex, v in enumerate(self._edgeIndices):
            yield self[faceEdgeIndex]

    # private

    def _getEdgeVertices(self, index):
        edgeIndex = self._edgeIndices[index]
        return self._objMesh.edges[edgeIndex].vertices

    @property
    def _edgeIndices(self):
        return self._objMesh.faces[self._faceIndex].edges


class MeshEdge:
    def __init__(self, index, objMesh, flipped=False):
        self._objMesh = objMesh
        self.index = index
        self.flipped = flipped

    def __getitem__(self, item):
        return self._objMesh.vertices[self._value.vertices[item]]

    def direction(self):
        begin, end = (self[0], self[1]) if not self.flipped else (self[1], self[0])
        return Vector(end) - Vector(begin)

    # private

    @property
    def _value(self):
        return self._objMesh.edges[self.index]


# private


class ObjMesh():
    def __init__(self, faces, edges, vertices, textureCoords):
        self.faces = faces
        self.edges = edges
        self.vertices = vertices
        self.textureCoords = textureCoords


class ObjFace():
    def __init__(self, edges, textureCoords):
        self.edges = edges
        self.textureCoords = textureCoords

    def __repr__(self):
        res = '(E = ['
        delim = ''
        for edge in self.edges:
            res += delim
            res += str(edge)
            delim = ', '
        res += '])'
        return res


class ObjEdge():
    def __init__(self, fst, snd):
        self.faces = []
        self.vertices = (fst, snd) if fst < snd else (snd, fst)

    def __hash__(self):
        return hash(self.vertices)

    def __eq__(self, other):
        return self.vertices == other.vertices

    def __repr__(self):
        return str(self.vertices)
