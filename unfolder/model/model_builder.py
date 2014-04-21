from unfolder.model.model_impl import ModelImpl, EdgeImpl, ConnectionImpl, \
    PatchImpl
from unfolder.util.appenders import IfNewAppender, MappingAppender, Appender, \
    BucketFiller


class ModelBuilder:
    def __init__(self, normal):
        self.normal = normal
        self.patches = BucketFiller()
        self.connections = MappingAppender()
        self.edges = IfNewAppender()
        self.vertices = IfNewAppender()
        self._nameMapping = {}

    def build(self):
        return ModelImpl(self.patches.store, None, self.connections.store, self.edges.store, self.vertices.store)

    def addVertex(self, vertex):
        return self.vertices.push(vertex)

    def addEdge(self, fstVertexIndex, sndVertexIndex):
        edge = EdgeImpl(fstVertexIndex, sndVertexIndex)
        return self.edges.push(edge)

    def addConnection(self, fstPatchName, sndPatchName, edgeIndices):
        connectionName = self._connectionName(fstPatchName, sndPatchName)
        return self.connections.push(connectionName, edgeIndices)

    def addPatch(self, patch: PatchImpl):
        return self.patches.put(patch.name, patch)

    def getConnection(self, fstPatchName, sndPatchName):
        connectionName = self._connectionName(fstPatchName, sndPatchName)
        return self.connections[connectionName]

    def getConnectionIndex(self, fstPatchName, sndPatchName):
        connectionName = self._connectionName(fstPatchName, sndPatchName)
        return self.connections.indexOf(connectionName)

    @staticmethod
    def _connectionName(fstName, sndName):
        return (sndName, fstName) if sndName > fstName else (fstName, sndName)
