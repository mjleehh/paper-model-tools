from maya.OpenMaya import MVector, MItMeshPolygon, MIntArray, MFnMesh, MItMeshVertex, MPoint, MItMeshEdge, MPointArray
from helpers import setIter


class CoordinateSystem:
    """ A 2D coordinate system with origin other than 0 in 3D space

    origin   the origin of the coordinate system realtive to global space
    e1, e2   orthogonal unit vectors
    """
    def __init__(self, origin, e1, e2):
        self.origin = origin
        self.e1 = e1
        self.e2 = e2

    def toLocal(self, vg):
        vLocalOrigin = vg - self.origin
        return (self.e1 * vLocalOrigin, self.e2 * vLocalOrigin)

    def toGlobal(self, vl):
        fst = MVector(self.e1)
        fst *= vl[0]
        snd =  MVector(self.e2)
        snd *= vl[1]
        trd = MVector(self.origin)
        vLocalOrigin = fst + snd
        return vLocalOrigin + trd


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


class Patch:
    def __init__(self, dagPath):
        self._dagPath = dagPath

    def createForTree(self, tree):
        mesh = MFnMesh()

        polyIter = MItMeshPolygon(self._dagPath)
        setIter(polyIter, tree.node)
        edges = MIntArray()
        polyIter.getEdges(edges)
        initialEdge = edges[0]

        self._create(tree, ConnectionEdge(initialEdge, MVector(0,0,0), MVector(1,0,0)), mesh)

    def _create(self, tree, connectionEdge, mesh):
        def mapVertex(vertexIndex):
            vertexIter = MItMeshVertex(self._dagPath)
            setIter(vertexIter, vertexIndex)
            vertex = vertexIter.position()
            localPosition = localCoordinateSystem.toLocal(vertex)
            globalPosition = globalCoodinateSystem.toGlobal(localPosition)
            return MPoint(globalPosition)

        def createFaces(faceIndex):
            edgeCycles = self._getEdgeCycles(faceIndex)
            newVertices = MPointArray()
            for edgeCycle in edgeCycles:
                vertexCycle = self._getVertexCycle(edgeCycle)
                for vertexIndex in vertexCycle:
                    newVertices.append(mapVertex(vertexIndex))
            mesh.addPolygon(newVertices)

        def getConnectionEdgeForEdge(edgeIndex):
            edgeIter = MItMeshEdge(self._dagPath)
            setIter(edgeIter, edgeIndex)
            begin = mapVertex(edgeIter.index(0))
            end = mapVertex(edgeIter.index(1))
            e1 = end - begin
            e1.normalize()
            return ConnectionEdge(edgeIndex, begin, e1)

        faceIndex = tree.node
        localCoordinateSystem = self._getCoordinateSystemForEdge(connectionEdge.index, faceIndex)
        e2 = connectionEdge.e1 ^ MVector(0,1,0)
        globalCoodinateSystem = CoordinateSystem(connectionEdge.origin, connectionEdge.e1, e2)

        createFaces(faceIndex)

        for child in tree.children:
            sharedEdge = self._getSharedEdge(faceIndex, child.node)
            connectionEdge = getConnectionEdgeForEdge(sharedEdge)
            self._create(child, connectionEdge, mesh)

    def _getSharedEdge(self, face, childFace):
        polyIter = MItMeshPolygon(self._dagPath)
        edges = MIntArray()
        setIter(polyIter, face)
        polyIter.getEdges(edges)
        childEdges = MIntArray()
        setIter(polyIter, childFace)
        polyIter.getEdges(childEdges)
        return (set(edges) & set(childEdges)).pop()

    def _getCoordinateSystemForEdge(self, edgeIndex, faceIndex):
        edgeIter = MItMeshEdge(self._dagPath)
        setIter(edgeIter, edgeIndex)
        polyIter = MItMeshPolygon(self._dagPath)
        setIter(polyIter,faceIndex)
        begin = edgeIter.point(0)
        end = edgeIter.point(1)
        e1 = end - begin
        e1.normalize()
        normal = MVector()
        polyIter.getNormal(normal)
        e2 = normal ^ e1
        e2.normalize()
        return CoordinateSystem(begin, e1, e2)

    def _getVertexCycle(self, edgeCycle):
        edgeIter = MItMeshEdge(self._dagPath)

        def getEdge(edgeIndex):
            setIter(edgeIter, edgeIndex)
            return (edgeIter.index(0), edgeIter.index(1))

        prevEdge = getEdge(edgeCycle[-1])
        retval = []
        for edgeIndex in edgeCycle:
            (fst, snd) = getEdge(edgeIndex)
            if fst in prevEdge:
                retval.append(fst)
            else:
                retval.append(snd)
            prevEdge = (fst, snd)
        return retval

    def _getEdgeCycles(self, poly):
        polyIter = MItMeshPolygon(self._dagPath)
        edgeIter = MItMeshEdge(self._dagPath)
        setIter(polyIter, poly)
        edgeIndices = MIntArray()
        polyIter.getEdges(edgeIndices)

        def getEdgeVertexIndices(edgeIndex):
            setIter(edgeIter, edgeIndex)
            return (edgeIter.index(0), edgeIter.index(1))

        prevEdgeIndex = edgeIndices[0]
        currentCyle = [prevEdgeIndex]
        retval = [currentCyle]

        for edgeIndex in edgeIndices[1:]:
            edge = getEdgeVertexIndices(edgeIndex)
            prevEdge = getEdgeVertexIndices(prevEdgeIndex)
            if set(prevEdge) & set(edge):
                currentCyle.append(edgeIndex)
            else:
                retval.append(currentCyle)
                currentCyle = [edgeIndex]
            prevEdgeIndex = edgeIndex

        for cyle in retval:
            firstEdge = getEdgeVertexIndices(cyle[0])
            lastEdge = getEdgeVertexIndices(cyle[1])
            if not (set(firstEdge) & set(lastEdge)):
                raise 'broken cycle detected!'
        return retval
