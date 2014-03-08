import maya.OpenMaya as om

from unfolder.util.plane_coordinate_system import PlaneCoordinateSystem
from unfolder.create_patch.patch_builder import MeshPatchBuilder


def boundingRects(mappingPlaneNormal, vertices):
    def coordinateSystemForConnectingVector(vertex1, vertex2):
        e1 = vertex2 - vertex1
        e1.normalize()
        e2 = e1 ^ om.MVector(mappingPlaneNormal)
        e2.normalize()

        return PlaneCoordinateSystem(vertex1, e1, e2)

    def getBoundingRect(coordinateSystem):
        boundingRect = om.MBoundingBox()

        for vertex in vertices:
            (x, y) = coordinateSystem.toLocal(vertex)
            boundingRect.expand(om.MPoint(x, y, 0))
        return boundingRect


    for i, vertex1 in enumerate(vertices):
        for vertex2 in vertices[i + 1:]:
            if not vertex1.isEquivalent(vertex2, 10E-5):
                coordinateSystem = coordinateSystemForConnectingVector(vertex1, vertex2)
                yield (getBoundingRect(coordinateSystem), coordinateSystem)

def fitOnPaper():

    activeSelection = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(activeSelection)

    selectedObjects = om.MItSelectionList(activeSelection, om.MFn.kMesh)
    fitObjectsInSelectionListOnPaper(selectedObjects)

    objectsWithSelectedFaces = om.MItSelectionList(activeSelection, om.MFn.kMeshVertComponent)
    fitObjectsInSelectionListOnPaper(objectsWithSelectedFaces)

def fitObjectsInSelectionListOnPaper(selectionListIter):
    def createMesh():
        mesh = om.MFnMesh()
        mesh.create(0, 0, om.MFloatPointArray(), om.MIntArray(), om.MIntArray())
        list = om.MSelectionList()
        list.add('initialShadingGroup')
        sg = om.MObject()
        list.getDependNode(0, sg)

        sgf = om.MFnSet(sg)
        sgf.addMember(mesh.object())

    while not selectionListIter.isDone():
        dagPath = om.MDagPath()
        components = om.MObject()
        selectionListIter.getDagPath(dagPath, components)

        vertexIter = om.MItMeshVertex(dagPath, components)
        vertices = []
        while not vertexIter.isDone():
            vertices.append(vertexIter.position(om.MSpace.kWorld))
            vertexIter.next()

        def areaIsGreater(lhs, rhs):
            def area(boundingRect):
                return boundingRect.width() * boundingRect.height()
            if area(rhs[0]) < area(lhs[0]):
                print(area(rhs[0]))
                return rhs
            else:
                print(area(lhs[0]))
                return lhs

        (rect, coords) = reduce(areaIsGreater, boundingRects(om.MVector(0,1,0), vertices))
        print(rect.width(), rect.height(), rect.depth())

        rectMin = rect.min()
        rectMax = rect.max()

        vertices = om.MPointArray()
        vertices.append(om.MPoint(coords.toGlobal((rectMin[0], rectMin[1]))))
        vertices.append(om.MPoint(coords.toGlobal((rectMax[0], rectMin[1]))))
        vertices.append(om.MPoint(coords.toGlobal((rectMax[0], rectMax[1]))))
        vertices.append(om.MPoint(coords.toGlobal((rectMin[0], rectMax[1]))))

        builder = MeshPatchBuilder()
        builder.addFace(0, vertices)

        selectionListIter.next()