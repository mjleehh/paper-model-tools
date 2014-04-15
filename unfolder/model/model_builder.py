from unfolder.model.model_impl import ModelImpl, EdgeImpl, ConnectionImpl
from unfolder.util.appenders import IfNewAppender, Appender


class ModelBuilder:
    def __init__(self, normal):
        self.normal = normal
        self.patches = []
        self.connections = Appender()
        self.edges = IfNewAppender()
        self.vertices = IfNewAppender()
        self._nameMapping = {}

    def build(self):
        return ModelImpl(self.patches, self.connections, self.edges, self.vertices)

    def addPatchName(self, patchName):
        if patchName in self._nameMapping:
            return self._nameMapping[patchName]
        else:
            index = len(self.patches)
            self.patches.append(None)
            self._nameMapping[patchName] = index
            return index

    def addVertex(self, vertex):
        return self.vertices.push(vertex)

    def addEdge(self, fstVertexIndex, sndVertexIndex):
        edge = EdgeImpl(fstVertexIndex, sndVertexIndex)
        self.edges.push(edge)

    def addConnection(self, fstEdgeIndices):
        return self.connections.push(ConnectionImpl(fstEdgeIndices))

    def addPatch(self, face, patch):
        patchIndex = len(self.patches)
        self.patches.append(patch)
        self._patchMapping[face] = patchIndex
        return patchIndex

    def getPatchIndex(self, face):
        if face in self._patchMapping:
            return self._patchMapping[face]
        else:
            return self.addPatch(face, None)
