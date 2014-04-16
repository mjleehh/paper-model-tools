from unfolder.model.model_impl import ModelImpl, EdgeImpl, ConnectionImpl
from unfolder.util.appenders import IfNewAppender, MappingAppender


class ModelBuilder:
    def __init__(self, normal):
        self.normal = normal
        self.patches = []
        self.connections = MappingAppender()
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

    def addConnection(self, fstPatchName, sndPatchName, fstEdgeIndices):
        connectionName = self._connectionName(fstPatchName, sndPatchName)
        return self.connections.push(connectionName, ConnectionImpl(fstEdgeIndices))

    def addPatch(self, face, patch):
        patchIndex = len(self.patches)
        self.patches.append(patch)
        self._patchMapping[face] = patchIndex
        return patchIndex

    def getConnection(self, fstPatchName, sndPatchName):
        connectionName = self._connectionName(fstPatchName, sndPatchName)
        return self.connections[connectionName]

    @staticmethod
    def _connectionName(self, fstName, sndName):
        return (sndName, fstName) if sndName > fstName else (fstName, sndName)
