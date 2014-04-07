from unfolder.mesh.obj_mesh import MeshEdge, Mesh, MeshFaces

from unfolder.tree.tree_impl import Node
from unfolder.model.model_impl import PatchEdge, ModelPatch, Model
from unfolder.util.plane_coordinate_system import PlaneCoordinateSystem
from unfolder.util.vector import Vector


def treeToModel(tree: Node, meshFaces):
    return TreeToModelConverter(meshFaces, None).convert(tree)

# private

class TreeToModelConverter:

    def __init__(self, meshFaces: MeshFaces, patchBuilder):
        self._meshFaces = meshFaces
        # the model normal
        self.modelBuilder = ModelBuilder((0., 1., 0.))

    def convert(self, tree: Node):
        # the model origin
        origin = (0., 0., 0.)
        fst = (1., 0., 0.)
        self.vertices = [origin, fst]
        inEdge = self._meshFaces[tree.index].edges[0]
        initialConnectionEdge = EdgeTransform([inEdge], self.vertices[0], self.vertices[1])

        self._flattenSubtree(tree, initialConnectionEdge)
        return self.modelBuilder.build()

    def _flattenSubtree(self, subtree, parentEdgeTransform):
        face = self._meshFaces[subtree.value]
        patchBuilder = PatchBuilder(face, parentEdgeTransform, self.modelBuilder)

        for child in subtree:
            edgeTransform = patchBuilder.getEdgeTransform(self._meshFaces[child.value])
            childPatchIndex = self._flattenSubtree(child, edgeTransform)
            patchBuilder.addSharedEdge(childPatchIndex, edgeTransform)

        a = set(face.getConnectedFaces())
        b = [self._meshFaces[child.value] for child in subtree]
        gluedFaces =  a - set(b)
        for gluedFace in gluedFaces:
            edgeTransform = patchBuilder.getEdgeTransform(gluedFace)
            gluedPatchIndex = self.modelBuilder.getPatchIndex(gluedFace)
            patchBuilder.addGlueEdge(gluedPatchIndex, edgeTransform)
        self.modelBuilder.addPatch(face, patchBuilder.build())


class PatchBuilder:
    def __init__(self, face, parentEdgeTransform, modelBuilder):
        self.face = face
        self._modelBuilder = modelBuilder
        self._edgeMapper = EdgeMapper(face, parentEdgeTransform, modelBuilder.normal)
        self.sharedEdges = []
        self.glueEdges = []
        self.borderEdges = []

    def build(self):
        return ModelPatch(None, self.sharedEdges, self.glueEdges, self.borderEdges)

    def addSharedEdge(self, childPatchIndex, edgeTransform):
        fstVertexIndex = self._modelBuilder.addVertex(tuple(edgeTransform.origin))
        sndVertexIndex = self._modelBuilder.addVertex(tuple(edgeTransform.e1))
        self.sharedEdges.append(PatchEdge(childPatchIndex, fstVertexIndex, sndVertexIndex))

    def addGlueEdge(self, gluedPatchIndex, edgeTransform):
        fstVertexIndex = self._modelBuilder.addVertex(tuple(edgeTransform.origin))
        sndVertexIndex = self._modelBuilder.addVertex(tuple(edgeTransform.e1))
        self.sharedEdges.append(PatchEdge(gluedPatchIndex, fstVertexIndex, sndVertexIndex))

    def getEdgeTransform(self, sndFace):
        inConnectingEdges = self.face.getConnectingEdges(sndFace)
        begin = self._edgeMapper.mapVertex(inConnectingEdges[0].begin)
        end = self._edgeMapper.mapVertex(inConnectingEdges[0].end)
        return EdgeTransform(inConnectingEdges, begin, end)


class ModelBuilder:
    def __init__(self, normal):
        self.normal = normal
        self.vertices = []
        self.patches = []
        self._vertexMapping = {}
        self._patchMapping = {}

    def build(self):
        return Model(self.patches, self.vertices)

    def addVertex(self, vertex):
        if vertex in self._vertexMapping:
            return self._vertexMapping[vertex]
        else:
            vertexIndex = len(self.vertices)
            self.vertices.append(vertex)
            self._vertexMapping[vertex] = vertexIndex
            return vertexIndex

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


class EdgeMapper:
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
    def __init__(self, inEdges, begin, end):
        self.inEdges = inEdges
        self.origin = Vector(begin)
        self.e1 = (Vector(end) - begin).normalized()
