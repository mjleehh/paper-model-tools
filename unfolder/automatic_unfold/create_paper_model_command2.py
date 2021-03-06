import maya.OpenMayaMPx as omp
import maya.OpenMaya as om
from unfolder.automatic_unfold.mesh_to_graph import meshToGraph
from unfolder.graph import GraphBuilder
from unfolder.mesh.maya_mesh import MeshFaces


class CreatePaperModelCommand2(omp.MPxCommand):

    def ___init__(self):
        omp.MPxCommand.__init__(self)

    def doIt(self, argList):
        self._flattenMesh()

    def _flattenMesh(self, strategy = None):
        """ Unfold mesh selection."""
        print("flattening selection")

        activeSelection = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(activeSelection)

        selectedObjects = om.MItSelectionList(activeSelection, om.MFn.kMesh)
        self._flattenObjectsInSelectionList(selectedObjects)

        objectsWithSelectedFaces = om.MItSelectionList(activeSelection, om.MFn.kMeshPolygonComponent)
        self._flattenObjectsInSelectionList(objectsWithSelectedFaces)

        print('flattening selection ... done')

    def _flattenObjectsInSelectionList(self, selectionListIter):
        while not selectionListIter.isDone():
            dagPath = om.MDagPath()
            components = om.MObject()
            selectionListIter.getDagPath(dagPath, components)
            print('flattening selection on object %(object)s' % {'object': dagPath.partialPathName()})
            self._flattenObject(dagPath, components)
            print('flattening faces for selected object ... done')
            selectionListIter.next()

    def _flattenObject(self, dagPath, components):
        if not components.isNull():
            print(components)
            faceIndices = om.MIntArray()
            om.MFnSingleIndexedComponent(components).getElements(faceIndices)
        else:
            faceIndices = range(om.MFnMesh(dagPath).numPolygons())

        faces = MeshFaces(dagPath, faceIndices)
        meshToGraph(faces, GraphBuilder())
