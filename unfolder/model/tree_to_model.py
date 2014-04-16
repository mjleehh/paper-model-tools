from unfolder.mesh.face import FaceIter, Face
from unfolder.model.model_builder import ModelBuilder

from unfolder.tree.tree_impl import Node
from unfolder.util.plane_coordinate_system import PlaneCoordinateSystem
from unfolder.util.vector import Vector


def treeToModel(tree: Node, meshFaces):
    return TreeToModelConverter(meshFaces, None).convert(tree)

# private

class TreeToModelConverter:
    def __init__(self, meshFaces: FaceIter, patchBuilder):
        self._meshFaces = meshFaces
        # the model normal
        self.modelBuilder = ModelBuilder((0., 1., 0.))

    def convert(self, tree: Node):
        # make all patch names known
        for name in tree.getNames():
            self.modelBuilder.addPatchName(name)
        # the model origin
        origin = (0., 0., 0.)
        fst = (1., 0., 0.)
        inEdge = self._meshFaces[tree.index].edges[0]
        initialConnectionEdge = EdgeTransform([inEdge], origin, fst)

        self._flattenSubtree(tree, None)
        return self.modelBuilder.build()

    def _flattenSubtree(self, subtree, parentFace):
        thisFace = self._meshFaces[subtree.value]
        patchBuilder = PatchBuilder(thisFace, parentFace, self.modelBuilder)

        for child in subtree:
            childFace = self._meshFaces[child.value]
            childConnectionIndex = patchBuilder.addConnection(childFace)
            self._flattenSubtree(child, thisFace)

        patchBuilder.build()

        #self.modelBuilder.addPatch(face, patchBuilder.build())

class PatchBuilder:
    def __init__(self, face: Face, parentFace, modelBuilder: ModelBuilder):
        self.face = face
        self._modelBuilder = modelBuilder
        self._vertexMapper = self._getVertexMapper(parentFace)
        self._edgeMapping = {}
        self._connections = []
        self._addEdges()

    def _getVertexMapper(self, parentFace):
        faceNormal = self._modelBuilder.normal
        modelNormal = self._modelBuilder.normal
        if parentFace:
            inConnectingEdge = self.face.getConnectingEdges(parentFace)[0]
            edgeIndex = self._modelBuilder.getConnection(self.face.index, parentFace.index).fstEdgeIndices[0]
            edge = self._modelBuilder.edges[edgeIndex]
            VertexMapper(faceNormal, inConnectingEdge, modelNormal)
        else:
            VertexMapper(faceNormal, self.face.edges[0], modelNormal)

    def addConnection(self, childFace):
        inConnectingEdges = self.face.getConnectingEdges(childFace)
        edgeIndices = [self._edgeMapping[inEdge.index] for inEdge in inConnectingEdges]
        connectionIndex =  self._modelBuilder.addConnection(self.face.index, childFace.index, edgeIndices)
        self._connections.append(connectionIndex)
        return connectionIndex

    def addGluedConnection(self, gluedPatchIndex):
        pass

    def build(self):
#        PatchImpl(self.face.index, self._connections, None)
        pass

    def _addEdges(self):
        for inFaceEdge in self.face.edges:
            fstVertexIndex = self._addVertex(inFaceEdge.begin)
            sndVertexIndex = self._addVertex(inFaceEdge.end)
            edgeIndex = self._modelBuilder.addEdge(fstVertexIndex, sndVertexIndex)
            self._edgeMapping[inFaceEdge.index] = edgeIndex

    def _addVertex(self, inVertex):
        vertex = tuple(self._vertexMapper.mapVertex(inVertex))
        return self._modelBuilder.addVertex(vertex)



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

class PatchEdgeProxy()