from unfolder.mesh.face import Face
from unfolder.model.model_builder import ModelBuilder
from unfolder.model.model_impl import PatchImpl
from unfolder.model.tree_to_model.edge_proxy import PatchEdgeProxy
from unfolder.model.tree_to_model.patch_base import PatchBase
from unfolder.model.tree_to_model.vertex_mapper import VertexMapper
from unfolder.util.appenders import MappingAppender


class PatchBuilder:
    def __init__(self, face: Face, patchBase: PatchBase, modelBuilder: ModelBuilder):
        self.face = face
        self.modelBuilder = modelBuilder
        self._parentConnection = patchBase.connection
        self._connections = MappingAppender()
        self._edgeMapping = {}
        self._edgeOrientation = {}
        self._vertexMapper = self._getVertexMapper(patchBase)
        self._addEdges(patchBase)

    def addConnection(self, childFace):
        inConnectingEdges = self.face.getConnectingEdges(childFace)
        inBaseEdge = inConnectingEdges[0]

        edgeIndices = [self._edgeMapping[inEdge.index] for inEdge in inConnectingEdges]
        connectionIndex =  self.modelBuilder.addConnection(edgeIndices)
        self._connections.push(childFace.index, connectionIndex)

        edgeIndex = edgeIndices[0]
        (fstVertexIndex, sndVertexIndex) = flipIf(self.modelBuilder.edges[edgeIndex].vertices,
                                                  self._edgeOrientation[inBaseEdge.index])
        begin = self.modelBuilder.vertices[fstVertexIndex]
        end = self.modelBuilder.vertices[sndVertexIndex]
        baseEdge = PatchEdgeProxy(begin, end)
        return PatchBase(connectionIndex, self.face, inBaseEdge, baseEdge)

    def build(self):
        freeEdgeIndices = self._getUnconnectedEdges()
        freeEdgeConnectionIndex =  self.modelBuilder.addConnection(freeEdgeIndices)
        connections = self._connections.store + [freeEdgeConnectionIndex] if freeEdgeConnectionIndex else self._connections.store
        return PatchImpl(self.face.index, self._parentConnection, connections, None)

    # private

    def _getUnconnectedEdges(self):
        allConnections = [self._parentConnection] + self._connections.store if self._parentConnection is not None else self._connections.store
        connectedEdgeIndices = set([edge for connectionIndex in allConnections for edge in self.modelBuilder.connections.store[connectionIndex]])
        return list(set(self._edgeMapping.values()) - connectedEdgeIndices)

    def _getVertexMapper(self, patchBase: PatchBase):
        faceNormal = self.face.normal
        modelNormal = self.modelBuilder.normal
        return VertexMapper(faceNormal, patchBase.inBaseEdge, modelNormal, patchBase.baseEdge)

    def _addEdges(self, patchBase):
        vertexMapper = self._getVertexMapper(patchBase)
        for inFaceEdge in self.face.edges:
            fstVertexIndex = self._addVertex(inFaceEdge.begin, vertexMapper)
            sndVertexIndex = self._addVertex(inFaceEdge.end, vertexMapper)
            flipped = fstVertexIndex > sndVertexIndex
            self._edgeOrientation[inFaceEdge.index] = flipped
            edgeIndex = self.modelBuilder.addEdge(fstVertexIndex, sndVertexIndex)
            self._edgeMapping[inFaceEdge.index] = edgeIndex

    def _addVertex(self, inVertex, vertexMapper):
        vertex = tuple(vertexMapper.mapVertex(inVertex))
        return self.modelBuilder.addVertex(vertex)


def flipIf(t, flip):
    return (t[1], t[0]) if flip else t