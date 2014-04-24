from unfolder.mesh.face import FaceIter, Face
from unfolder.model.tree_to_model.edge_proxy import PatchEdgeProxy
from unfolder.model.model import Model
from unfolder.model.model_builder import ModelBuilder
from unfolder.model.model_impl import PatchImpl
from unfolder.model.tree_to_model.vertex_mapper import VertexMapper

from unfolder.tree.knot import Knot
from unfolder.util.appenders import MappingAppender


def treeToModel(tree: Knot, meshFaces):
    return TreeToModelConverter(meshFaces, None).convert(tree)

# private

class TreeToModelConverter:
    def __init__(self, meshFaces: FaceIter, patchBuilder):
        self._meshFaces = meshFaces
        # the model normal
        self.modelBuilder = ModelBuilder((0., 0., 1.))

    def convert(self, tree: Knot):
        origin = (0., 0., 0.)
        fst = (1., 0., 0.)
        baseEdge = PatchEdgeProxy(origin, fst)
        inBaseEdge = self._meshFaces[tree.value].edges[0]
        self._flattenSubtree(tree, PatchBase(None, None, inBaseEdge, baseEdge))
        return Model(self.modelBuilder.build())

    def _flattenSubtree(self, subtree, patchBase):
        thisFace = self._meshFaces[subtree.value]
        patchBuilder = PatchBuilder(thisFace, patchBase, self.modelBuilder)

        children = set()

        for child in subtree:
            childFace = self._meshFaces[child.value]
            children.add(childFace)
            print(str(thisFace.index) + ' -> ' + str(childFace.index))
            childPatchBase = patchBuilder.addConnection(childFace)
            self._flattenSubtree(child, childPatchBase)

        connectedFaces = set(thisFace.getConnectedFaces()) - children
        if patchBase.parentFace is not None:
            connectedFaces.remove(patchBase.parentFace)

        for face in connectedFaces:
            print(face.index)

        self.modelBuilder.addPatch(patchBuilder.build())


class PatchBase:
    def __init__(self, connection, parentFace, inBaseEdge, baseEdge):
        self.connection = connection
        self.parentFace = parentFace
        self.inBaseEdge = inBaseEdge
        self.baseEdge = baseEdge


def flipIf(t, flip):
    return (t[1], t[0]) if flip else t


class PatchBuilder:
    def __init__(self, face: Face, patchBase: PatchBase, modelBuilder: ModelBuilder):
        self.face = face
        self.modelBuilder = modelBuilder
        self._vertexMapper = self._getVertexMapper(patchBase)
        self._edgeMapping = {}
        self._edgeOrientation = {}
        self._patchBase = patchBase
        self._connections = MappingAppender()
        self._addEdges()

    def _getVertexMapper(self, patchBase: PatchBase):
        faceNormal = self.face.normal
        modelNormal = self.modelBuilder.normal
        return VertexMapper(faceNormal, patchBase.inBaseEdge, modelNormal, patchBase.baseEdge)

    def addConnection(self, childFace):
        inConnectingEdges = self.face.getConnectingEdges(childFace)
        inBaseEdge = inConnectingEdges[0]

        edgeIndices = [self._edgeMapping[inEdge.index] for inEdge in inConnectingEdges]
        connectionIndex =  self.modelBuilder.addConnection(self.face.index, childFace.index, edgeIndices)
        self._connections.push(childFace.index, connectionIndex)

        edgeIndex = edgeIndices[0]
        (fstVertexIndex, sndVertexIndex) = flipIf(self.modelBuilder.edges[edgeIndex].vertices,
                                                  self._edgeOrientation[inBaseEdge.index])
        begin = self.modelBuilder.vertices[fstVertexIndex]
        end = self.modelBuilder.vertices[sndVertexIndex]
        baseEdge = PatchEdgeProxy(begin, end)
        return PatchBase(connectionIndex, self.face, inBaseEdge, baseEdge)

    def build(self):
        return PatchImpl(self.face.index, self._patchBase.connection, self._connections.store, None)

    def _addEdges(self):
        for inFaceEdge in self.face.edges:
            fstVertexIndex = self._addVertex(inFaceEdge.begin)
            sndVertexIndex = self._addVertex(inFaceEdge.end)
            flipped = fstVertexIndex > sndVertexIndex
            self._edgeOrientation[inFaceEdge.index] = flipped
            edgeIndex = self.modelBuilder.addEdge(fstVertexIndex, sndVertexIndex)
            self._edgeMapping[inFaceEdge.index] = edgeIndex

    def _addVertex(self, inVertex):
        vertex = tuple(self._vertexMapper.mapVertex(inVertex))
        print('v: ' + str(inVertex) + ' => ' + str(vertex))
        return self.modelBuilder.addVertex(vertex)
