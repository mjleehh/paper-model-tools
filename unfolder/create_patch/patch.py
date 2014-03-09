from maya.OpenMaya import MVector, MItMeshPolygon, MIntArray, MItMeshVertex, MPoint, MItMeshEdge, MPointArray
from unfolder.util.plane_coordinate_system import PlaneCoordinateSystem
from unfolder.util.helpers import setIter


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

    def flattenSubtree(subtree, connectionEdge, mappingPlaneNormal, patchBuilder):
        def mapVertex(vertexIndex):
            vertexIter = MItMeshVertex(dagPath)
            setIter(vertexIter, vertexIndex)
            vertex = vertexIter.position()
            localPosition = localCoordinateSystem.toLocal(vertex)
            globalPosition = globalCoodinateSystem.toGlobal(localPosition)
            return MPoint(globalPosition)

        def createFaces(faceIndex):
            edgeCycles = getEdgeCycles(faceIndex)
            newVertices = MPointArray()
            for edgeCycle in edgeCycles:
                vertexCycle = getVertexCycle(edgeCycle)
                for vertexIndex in vertexCycle:
                    newVertices.append(mapVertex(vertexIndex))
            patchBuilder.addFace(faceIndex, newVertices)

        def getConnectionEdgeForEdge(edgeIndex):
            edgeIter = MItMeshEdge(dagPath)
            setIter(edgeIter, edgeIndex)
            begin = mapVertex(edgeIter.index(0))
            end = mapVertex(edgeIter.index(1))
            e1 = end - begin
            e1.normalize()
            return ConnectionEdge(edgeIndex, begin, e1)

        faceIndex = subtree.face
        localCoordinateSystem = getFacePlaneCoordinateSystemForFaceEdge(connectionEdge.index, faceIndex)
        e2 = connectionEdge.e1 ^ mappingPlaneNormal
        globalCoodinateSystem = PlaneCoordinateSystem(connectionEdge.origin, connectionEdge.e1, e2)

        createFaces(faceIndex)

        for child in subtree.children:
            sharedEdge = getSharedEdge(faceIndex, child.face)
            connectionEdge = getConnectionEdgeForEdge(sharedEdge)
            flattenSubtree(child, connectionEdge, mappingPlaneNormal, patchBuilder)

    def getSharedEdge(face, childFace):
        """ Get one of the edges that two faces share.

        The edge returned is simply the first edge in the intersection.

        Note: When placing two faces in a 2D plane preserving one shared edge
        preserves all shared edges.
        """
        polyIter = MItMeshPolygon(dagPath)
        edges = MIntArray()
        setIter(polyIter, face)
        polyIter.getEdges(edges)
        childEdges = MIntArray()
        setIter(polyIter, childFace)
        polyIter.getEdges(childEdges)
        return (set(edges) & set(childEdges)).pop()

    def getFacePlaneCoordinateSystemForFaceEdge(edgeIndex, faceIndex):
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
        edgeIter = MItMeshEdge(dagPath)
        setIter(edgeIter, edgeIndex)
        polyIter = MItMeshPolygon(dagPath)
        setIter(polyIter,faceIndex)
        begin = edgeIter.point(0)
        end = edgeIter.point(1)
        e1 = end - begin
        e1.normalize()
        normal = MVector()
        polyIter.getNormal(normal)
        e2 = normal ^ e1
        e2.normalize()
        return PlaneCoordinateSystem(begin, e1, e2)

    def getVertexCycle(edgeCycle):
        """ Returns a vertex cycle for a face from its edge cycles.

        A face has several vertex cycles. These vertex cycles determine the edge
        ordering in the face.

        - The first vertex cycle describes the face boundary. It is in counter
          clockwise order.
        - All other vertex cycles describe holes in the face. These cycles are
          in clockwise order.
        """
        edgeIter = MItMeshEdge(dagPath)

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

    def getEdgeCycles(poly):
        polyIter = MItMeshPolygon(dagPath)
        edgeIter = MItMeshEdge(dagPath)
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

    polyIter = MItMeshPolygon(dagPath)
    setIter(polyIter, tree.face)
    edges = MIntArray()
    polyIter.getEdges(edges)
    initialEdge = edges[0]

    mappingPlaneOrigin = MVector(0, 0, 0)
    mappingPlaneNormal = MVector(0, 1, 0)
    mappedInitialEdgeDirection = MVector(1, 0, 0)
    initialConnectionEdge = ConnectionEdge(initialEdge, mappingPlaneOrigin, mappedInitialEdgeDirection)

    flattenSubtree(tree, initialConnectionEdge, mappingPlaneNormal, patchBuilder)
