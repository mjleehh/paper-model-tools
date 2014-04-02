from .face_utils import *

import numpy as np

class ConnectionEdge:
    """ The edge that connects two faces.

    index   the index of the edge in the mesh
    origin  the position of the first vertex after mapping
    e1      the normalized edge direction vector after mapping
    """
    def __init__(self, index, origin, e1):
        self.index = index
        self.origin = origin
        self.e1 = e1

def flattenTree(dagPath, tree, patchBuilder):
    return PatchBuilder(dagPath, patchBuilder).buildPatch(tree)


class PatchBuilder:

    def __init__(self, mesh, patchBuilder):

        self._patchBuilder = patchBuilder
        # the patch normal
        self.normal = mappingPlaneNormal = (0, 1, 0)
        # the patch origin
        mappingPlaneOrigin = (0, 0, 0)


    def buildPatch(self, tree):

        initialEdge = edges[0]
        initialPatchEdge = (1, 0, 0)
        initialConnectionEdge = ConnectionEdge(initialEdge, mappingPlaneOrigin, mappedInitialEdgeDirection)

        self._flattenSubtree(tree, initialConnectionEdge, mappingPlaneNormal)


    def _flattenSubtree(self, subtree, connectionEdge, mappingPlaneNormal):
        faceIndex = subtree.value
        localCoordinateSystem = getFacePlaneCoordinateSystemForFaceEdge(connectionEdge.index, faceIndex, self._dagPath)

        globalCoodinateSystem = PlaneCoordinateSystem(connectionEdge.origin, connectionEdge.e1, e2)

        createFace()

        for child in subtree:
            sharedEdge = getSharedEdge(faceIndex, child.face, self._dagPath)
            connectionEdge = getConnectionEdgeForEdge(sharedEdge)
            self._flattenSubtree(child, connectionEdge, mappingPlaneNormal)

    def getEdgeInPlaneNormal(self, patchEdge):
        e2 = np.cross(patchEdge.e1, self.normal)

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