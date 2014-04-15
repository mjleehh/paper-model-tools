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

        self._flattenSubtree(tree, initialConnectionEdge)
        return self.modelBuilder.build()

    def _flattenSubtree(self, subtree, parentEdgeTransform):
        face = self._meshFaces[subtree.value]
        patchBuilder = PatchBuilder(face, parentEdgeTransform, self.modelBuilder)

        for child in subtree:
            childFace = self._meshFaces[child.value]
            edgeTransform = patchBuilder.addConnection(childFace)
            self._flattenSubtree(child, edgeTransform)

        patchBuilder.build()

        #self.modelBuilder.addPatch(face, patchBuilder.build())

    def getEdgeTransform(self, sndFace):
        inConnectingEdges = self.face.getConnectingEdges(sndFace)
        begin = self._vertexMapper.mapVertex(inConnectingEdges[0].begin)
        end = self._vertexMapper.mapVertex(inConnectingEdges[0].end)
        return EdgeTransform(inConnectingEdges, begin, end)


class PatchBuilder:
    def __init__(self, face: Face, parentEdgeTransform, modelBuilder):
        self.face = face
        self._modelBuilder = modelBuilder
        self._vertexMapper = VertexMapper(face, parentEdgeTransform, modelBuilder.normal)
        self._edgeMapping = {}
        self._connections = []
        self._addEdges()

    def addConnection(self, childFace):
        #edgeTransform = self.getEdgeTransform(childFace)
        inConnectingEdges = self.face.getConnectingEdges(childFace)
        edgeIndices = [self._edgeMapping[inEdge.index] for inEdge in inConnectingEdges]
        connectionIndex =  self._modelBuilder.addConnection(edgeIndices)
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
    def __init__(self, inFace, connectingEdges, normal):
        self._inFaceCoordinateSystem = self._getInFaceCoordinateSystemAtEdge(inFace, connectingEdges.inEdges[0])
        self._patchCoordinateSystem = self._getPatchCoordinateSystem(normal, connectingEdges)

    def mapVertex(self, vertex):
        faceCoords = self._inFaceCoordinateSystem.toLocal(vertex)
        patchCoords = self._patchCoordinateSystem.toGlobal(faceCoords)
        return patchCoords

    def _getPatchCoordinateSystem(self, modelNormal, connectionEdge):
        e2 = connectionEdge.e1 ^ modelNormal
        return PlaneCoordinateSystem(connectionEdge.origin, connectionEdge.e1, e2)

    def _getInFaceCoordinateSystemAtEdge(self, inFace, inEdge):
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
        e1 = inEdge.direction.normalized()
        faceNormal = inFace.getNormal()
        e2 = (e1 ^ faceNormal).normalized()
        return PlaneCoordinateSystem(inEdge.begin, e1, e2)


class EdgeTransform:
    """ The edge that connects two faces.

    inEdges   the unmapped edges
    origin    the position of the first vertex after mapping
    e1        the normalized edge direction vector after mapping
    """
    def __init__(self, connectionIndex, begin, end):
        self.connectionIndex = connectionIndex
        self.origin = Vector(begin)
        self.e1 = (Vector(end) - begin).normalized()
