from unfolder.util.plane_coordinate_system import PlaneCoordinateSystem

from .face_utils import *


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

    def __init__(self, dagPath, patchBuilder):
        self._dagPath = dagPath
        self._patchBuilder = patchBuilder

    def buildPatch(self, tree):

        polyIter = om.MItMeshPolygon(self._dagPath)
        setIter(polyIter, tree.face)
        edges = om.MIntArray()
        polyIter.getEdges(edges)
        initialEdge = edges[0]

        mappingPlaneOrigin = om.MVector(0, 0, 0)
        mappingPlaneNormal = om.MVector(0, 1, 0)
        mappedInitialEdgeDirection = om.MVector(1, 0, 0)
        initialConnectionEdge = ConnectionEdge(initialEdge, mappingPlaneOrigin, mappedInitialEdgeDirection)

        self._flattenSubtree(tree, initialConnectionEdge, mappingPlaneNormal)


    def _flattenSubtree(self, subtree, connectionEdge, mappingPlaneNormal):
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

        faceIndex = subtree.face
        localCoordinateSystem = getFacePlaneCoordinateSystemForFaceEdge(connectionEdge.index, faceIndex, self._dagPath)
        e2 = connectionEdge.e1 ^ mappingPlaneNormal
        globalCoodinateSystem = PlaneCoordinateSystem(connectionEdge.origin, connectionEdge.e1, e2)

        createFace()

        for child in subtree.children:
            sharedEdge = getSharedEdge(faceIndex, child.face, self._dagPath)
            connectionEdge = getConnectionEdgeForEdge(sharedEdge)
            self._flattenSubtree(child, connectionEdge, mappingPlaneNormal)


