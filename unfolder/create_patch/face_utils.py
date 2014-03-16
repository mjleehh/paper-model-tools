import maya.OpenMaya as om

from unfolder.util.helpers import setIter
from unfolder.util.plane_coordinate_system import PlaneCoordinateSystem


def getSharedEdge(face, childFace, dagPath):
    """ Get one of the edges that two faces share.

    The edge returned is simply the first edge in the intersection.

    Note: When placing two faces in a 2D plane preserving one shared edge
    preserves all shared edges.
    """
    polyIter = om.MItMeshPolygon(dagPath)
    edges = om.MIntArray()
    setIter(polyIter, face)
    polyIter.getEdges(edges)
    childEdges = om.MIntArray()
    setIter(polyIter, childFace)
    polyIter.getEdges(childEdges)
    return (set(edges) & set(childEdges)).pop()


def getFacePlaneCoordinateSystemForFaceEdge(edgeIndex, faceIndex, dagPath):
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
    edgeIter = om.MItMeshEdge(dagPath)
    setIter(edgeIter, edgeIndex)
    polyIter = om.MItMeshPolygon(dagPath)
    setIter(polyIter,faceIndex)
    begin = edgeIter.point(0)
    end = edgeIter.point(1)
    e1 = end - begin
    e1.normalize()
    normal = om.MVector()
    polyIter.getNormal(normal)
    e2 = normal ^ e1
    e2.normalize()
    return PlaneCoordinateSystem(begin, e1, e2)

def getVertexCycle(edgeCycle, dagPath):
    """ Returns a vertex cycle for a face from its edge cycles.

    A face has several vertex cycles. These vertex cycles determine the edge
    ordering in the face.

    - The first vertex cycle describes the face boundary. It is in counter
      clockwise order.
    - All other vertex cycles describe holes in the face. These cycles are
      in clockwise order.
    """
    edgeIter = om.MItMeshEdge(dagPath)

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


def getEdgeCycles(face, dagPath):
    """ Returns a edge cycle for a face.

    A face has several edge cycles:

    - The first edge cycle describes the face boundary. It is in counter
      clockwise order.
    - All other edge cycles describe holes in the face. These cycles are
      in clockwise order.
    """
    faceIter = om.MItMeshPolygon(dagPath)
    edgeIter = om.MItMeshEdge(dagPath)
    setIter(faceIter, face)
    edgeIndices = om.MIntArray()
    faceIter.getEdges(edgeIndices)

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