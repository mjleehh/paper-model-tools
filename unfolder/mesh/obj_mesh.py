class Mesh_Faces:

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
        pass


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
