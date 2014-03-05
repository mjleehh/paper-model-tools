import maya.OpenMaya as om

from helpers import vprint


from coordinatesystem import CoordinateSystem


def getMinimumSurfaceAreaForGeometry(mappingPlaneNormal, vertices):
    def getAreaForRect(vertex1, vertex2, vertices):
        e1 = vertex2 - vertex1
        e1.normalize()
        e2 = e1 ^ mappingPlaneNormal
        e2.nomalize()

        coordinateSystem = CoordinateSystem(vertex1, e1, e2)
        for vertex in vertices:
            coordinateSystem.toLocal(vertex)

    for i, vertex1 in enumerate(vertices):
        for vertex2 in vertices[i + 1:]:
            print(vertex1, vertex2)
            yield (vertex1, vertex2)

def fitOnPaper():

    activeSelection = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(activeSelection)

    selectedObjects = om.MItSelectionList(activeSelection, om.MFn.kMesh)
    fitObjectsInSelectionListOnPaper(selectedObjects)

    objectsWithSelectedFaces = om.MItSelectionList(activeSelection, om.MFn.kMeshVertComponent)
    fitObjectsInSelectionListOnPaper(objectsWithSelectedFaces)

def fitObjectsInSelectionListOnPaper(selectionListIter):
    while not selectionListIter.isDone():
        dagPath = om.MDagPath()
        components = om.MObject()
        selectionListIter.getDagPath(dagPath, components)

        vertexIter = om.MItMeshVertex(dagPath, components)
        vertices = []
        while not vertexIter.isDone():
            vertices.append(vertexIter.position())
            vertexIter.next()

        for pair in getMinimumSurfaceAreaForGeometry((0,1,0), vertices):
            print(pair)

        selectionListIter.next()