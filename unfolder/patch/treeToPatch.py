import numpy as np
from unfolder.patch.patch2 import PatchEdge, PatchFace


def treeToPatch(tree, meshFaces):
    return TreeToPatchConverter(meshFaces, None).buildPatch(tree)

# private

class MappedEdge:
    """ The edge that connects two faces.

    edge    the edge
    origin  the position of the first vertex after mapping
    e1      the normalized edge direction vector after mapping
    """
    def __init__(self, index, origin, e1):
        self.index = index
        self.origin = origin
        self.e1 = e1


class TreeToPatchConverter:

    def __init__(self, meshFaces, patchBuilder):
        self._meshFaces = meshFaces
        self._patchBuilder = patchBuilder
        # the patch normal
        self.normal = np.array((0, 1, 0))

        self.vertices = []
        self._faceMapping = {}
        self.faces = []

    def buildPatch(self, tree):
        # the patch origin
        origin = np.array((0, 0, 0))
        self.vertices = [origin, origin + (1, 0, 0)]
#       initialEdge =
        initialPatchEdge = PatchEdge(None, 0, 1)
        initialConnectionEdge = MappedEdge(0, origin, initialPatchEdge)

        self._flattenSubtree(tree, initialConnectionEdge)


    def _flattenSubtree(self, subtree, connectionEdge):
        inFaceIndex = subtree.value
        inFace = self._meshFaces[inFaceIndex]
        parentEdge = None
        edges = []

        localCoordinateSystem = self.getFacePlaneCoordinateSystemForFaceEdge(connectionEdge.index, inFace)

        #globalCoodinateSystem = PlaneCoordinateSystem(connectionEdge.origin, connectionEdge.e1, e2)

        inChildFaceIndices = []
        inMeshIndices = inFace.edgeIndices

        for child in subtree:
            inChildFaceIndex = child.value
            inChildFaceIndices.append(inChildFaceIndex)
            inChildFace = self._meshFaces[inChildFaceIndex]
            connectionEdge = None #getConnectionEdgeForEdge(sharedEdge)
            self._flattenSubtree(child, connectionEdge)


        self._faceMapping[inFaceIndex] = len(self.faces)
        self.faces.append(PatchFace(parentEdge, edges))

    def _getFace(self, meshFaceIndex):
        if meshFaceIndex in self._faceMapping:
            return self._faceMapping[meshFaceIndex]
        else:
            index = len(self.faces)
            self._faceMapping[meshFaceIndex] = index
            self.faces.append(None)
            return index

    def getEdgeInPlaneNormal(self, patchEdge):
        e2 = np.cross(patchEdge.e1, self.normal)

    def getFacePlaneCoordinateSystemForFaceEdge(self, edge, face):
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
        (begin, end) = edge
        e1 = end - begin
        e1.normalize()
        normal = face.getNormal()
        e2 = np.cross(normal, e1)
        e2.normalize()
        return PlaneCoordinateSystem(begin, e1, e2)

#############################################

        def mapVertex(vertexIndex):
            vertexIter = om.MItMeshVertex(self._dagPath)
            setIter(vertexIter, vertexIndex)
            vertex = vertexIter.position()
            localPosition = localCoordinateSystem.toLocal(vertex)
            globalPosition = globalCoodinateSystem.toGlobal(localPosition)
            return om.MPoint(globalPosition)

        def createFace():
            edgeCycles = getEdgeCycles(faceIndex, self._dagPath)
            newVertices = om.MPointArray()
            for edgeCycle in edgeCycles:
                vertexCycle = getVertexCycle(edgeCycle, self._dagPath)
                for vertexIndex in vertexCycle:
                    newVertices.append(mapVertex(vertexIndex))
            self._patchBuilder.addFace(faceIndex, newVertices)

        def getConnectionEdgeForEdge(edgeIndex):
            edgeIter = om.MItMeshEdge(self._dagPath)
            setIter(edgeIter, edgeIndex)
            begin = mapVertex(edgeIter.index(0))
            end = mapVertex(edgeIter.index(1))
            e1 = end - begin
            e1.normalize()
            return ConnectionEdge(edgeIndex, begin, e1)