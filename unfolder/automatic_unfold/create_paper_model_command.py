import maya.OpenMayaMPx as omp
import maya.OpenMaya as om

from .test_collision import detectCollision

from unfolder.model.patch_old import flattenTree
from unfolder.model.model_builder_old import MeshPatchBuilder

from .generate_facetree import createFacetreeLightning
from .selected_faces import findConnectedFaces


class CreatePaperModelCommand(omp.MPxCommand):
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
        connectedFaceSets = findConnectedFaces(dagPath, components)
        for connectedFaceSet in connectedFaceSets:
            tree = createFacetreeLightning(dagPath, connectedFaceSet)
            patchBuilder = MeshPatchBuilder()
            flattenTree(dagPath, tree, patchBuilder)
            detectCollision(patchBuilder.mesh)


