from unfolder.mesh.face import FaceIter, Face
from unfolder.model.model import Model
from unfolder.model.model_builder import ModelBuilder
from unfolder.model.model_impl import PatchImpl

from unfolder.tree.knot import Knot
from unfolder.util.plane_coordinate_system import PlaneCoordinateSystem
from unfolder.util.vector import Vector


def treeToModel(tree: Knot, meshFaces):
    return TreeToModelConverter(meshFaces, None).convert(tree)

# private

class TreeToModelConverter:
    def __init__(self, meshFaces: FaceIter, patchBuilder):
        self._meshFaces = meshFaces
        # the model normal
        self.modelBuilder = ModelBuilder((0., 1., 0.))

    def convert(self, tree: Knot):
        self._flattenSubtree(tree, None)
        return Model(self.modelBuilder.build())

    def _flattenSubtree(self, subtree, parentFace):
        thisFace = self._meshFaces[subtree.value]
        patchBuilder = PatchBuilder(thisFace, parentFace, self.modelBuilder)

        for child in subtree:
            childFace = self._meshFaces[child.value]
            patchBuilder.addConnection(childFace)
            self._flattenSubtree(child, thisFace)

        self.modelBuilder.addPatch(patchBuilder.build())

class PatchBuilder:
    def __init__(self, face: Face, parentFace: Face, modelBuilder: ModelBuilder):
        self.face = face
        self.modelBuilder = modelBuilder
        self._vertexMapper = self._getVertexMapper(parentFace)
        self._edgeMapping = {}
        self._parentConnection = None if parentFace is None \
            else self.modelBuilder.getConnectionIndex(face.index, parentFace.index)
        self._connections = []
        self._addEdges()

    def _getVertexMapper(self, parentFace: Face):
        faceNormal = self.modelBuilder.normal
        modelNormal = self.modelBuilder.normal
        if parentFace:
            inConnectingEdge = self.face.getConnectingEdges(parentFace)[0]
            edgeIndex = self.modelBuilder.getConnection(self.face.index, parentFace.index)[0]
            (fstVertexIndex, sndVertexIndex) = self.modelBuilder.edges[edgeIndex].vertices
            begin = self.modelBuilder.vertices[fstVertexIndex]
            end = self.modelBuilder.vertices[sndVertexIndex]
            return VertexMapper(faceNormal, inConnectingEdge, modelNormal, PatchEdgeProxy(begin, end))
        else:
            origin = (0., 0., 0.)
            fst = (1., 0., 0.)
            return VertexMapper(faceNormal, self.face.edges[0], modelNormal, PatchEdgeProxy(origin, fst))

    def addConnection(self, childFace):
        inConnectingEdges = self.face.getConnectingEdges(childFace)
        edgeIndices = [self._edgeMapping[inEdge.index] for inEdge in inConnectingEdges]
        connectionIndex =  self.modelBuilder.addConnection(self.face.index, childFace.index, edgeIndices)
        self._connections.append(connectionIndex)
        return connectionIndex

    def addShadowPatch(self, gluedPatchIndex):
        pass

    def build(self):
        return PatchImpl(self.face.index, self._parentConnection, self._connections, None)

    def _addEdges(self):
        for inFaceEdge in self.face.edges:
            fstVertexIndex = self._addVertex(inFaceEdge.begin)
            sndVertexIndex = self._addVertex(inFaceEdge.end)
            edgeIndex = self.modelBuilder.addEdge(fstVertexIndex, sndVertexIndex)
            self._edgeMapping[inFaceEdge.index] = edgeIndex

    def _addVertex(self, inVertex):
        vertex = tuple(self._vertexMapper.mapVertex(inVertex))
        return self.modelBuilder.addVertex(vertex)



class VertexMapper:
    """ Determine the 2D coordinate system for one of the face edges

        The 2d coordinate system spans the face plane:
        - the origin is the first vertex of the edge
        - the first unit vector is the normalized vector from the first edge
          vertex to the second edge vertex
        - the second unit vector is the normalized vector directed at n x e_1

        Faces in maya have counter clockwise vertex order. Thus e_2 faces
        'into' the face area. The three vectors (e_1, e_2, n) for right handed
        coordinates for the 3D space (e_1 x e_2 = n).
    """
    def __init__(self, faceNormal, inEdge, modelNormal, mappedEdge):
        self._inFaceCoordinateSystem = self._getCoordinateSystemForEdge(inEdge, faceNormal)
        self._patchCoordinateSystem = self._getCoordinateSystemForEdge(mappedEdge, modelNormal)

    def mapVertex(self, vertex):
        faceCoords = self._inFaceCoordinateSystem.toLocal(vertex)
        patchCoords = self._patchCoordinateSystem.toGlobal(faceCoords)
        return patchCoords

    def _getCoordinateSystemForEdge(self, edge, normal):
        origin = edge.begin
        e1 = edge.direction.normalized()
        e2 = (e1 ^ normal).normalized()
        return PlaneCoordinateSystem(origin, e1, e2)


class PatchEdgeProxy():
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    @property
    def direction(self):
        return Vector(self.end) - Vector(self.begin)