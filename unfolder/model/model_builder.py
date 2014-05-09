from unfolder.model.model_impl import ModelImpl, EdgeImpl, PatchImpl
from unfolder.util.appenders import VertexAppender, MappingAppender, Appender, \
    BucketFiller, NewAppender


class ModelBuilder:
    def __init__(self, normal):
        self.normal = normal
        self.patches = BucketFiller()
        self.connections = Appender()
        self.edges = NewAppender()
        self.vertices = VertexAppender()
        self._nameMapping = {}

    def build(self):
        return ModelImpl(self.patches.store, None, self.connections.store, self.edges.store, self.vertices.store)

    def addVertex(self, vertex):
        return self.vertices.push(vertex)

    def addEdge(self, fstVertexIndex, sndVertexIndex):
        edge = EdgeImpl(fstVertexIndex, sndVertexIndex)
        return self.edges.push(edge)

    def addConnection(self, edgeIndices):
        return self.connections.push(edgeIndices)

    def addPatch(self, patch: PatchImpl):
        return self.patches.put(patch.name, patch)

