import maya.OpenMaya as om
from unfolder.analyze_patch.inner_vertex_checker import InnerVertexChecker
from unfolder.util.helpers import setIter


def detectCollision(mesh):
    dagPath = om.MDagPath()
    mesh.getPath(dagPath)
    faceIter = om.MItMeshPolygon(dagPath)
    vertexIter = om.MItMeshVertex(dagPath)
    edgeIter = om.MItMeshEdge(dagPath)

    vertices = []
    while not vertexIter.isDone():
        vertex = vertexIter.position()
        vertices.append(vertex)
        vertexIter.next()

    result = False
    while not faceIter.isDone():
        edgesIndices = om.MIntArray()
        faceIter.getEdges(edgesIndices)

        edges = []
        for edgeIndex in edgesIndices:
            setIter(edgeIter, edgeIndex)
            vertex1 = edgeIter.point(0)
            vertex2 = edgeIter.point(1)
            edges.append((to2d(vertex1), to2d(vertex2)))

        checker = InnerVertexChecker(edges)

        for vertex in vertices:
            if checker.isInnerVertex(vertex):
                print('collision')
                return True
        print(result)
        faceIter.next()
    print('no collision')
    return False

def to2d(vertex):
    return (vertex(0), vertex(2))