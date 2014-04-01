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
        pass

    def getConnectedFaces(self):
        face = self._objMesh.faces[self.index]
        return [MeshFace(self._objMesh, faceIndex) for edge in face.edges for faceIndex in self._objMesh.edges[edge].faces if faceIndex != self.index]


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
