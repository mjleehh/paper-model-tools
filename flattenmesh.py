from maya.OpenMaya import MSelectionList, MItSelectionList, MDagPath, MObject, MFn, MGlobal

from connectedfaces import findConnectedFaces
from facetree import createFacetreeLightning
from facetree import createFacetreeSpiral
from patch import flattenTree, MeshPatchBuilder


def flattenMesh(strategy = None):
    """ Unfold mesh selection."""
    print("flattening selection")

    activeSelection = MSelectionList()
    MGlobal.getActiveSelectionList(activeSelection)

    selectedObjects = MItSelectionList(activeSelection, MFn.kMesh)
    flattenObjectsInSelectionList(selectedObjects, strategy)

    objectsWithSelectedFaces = MItSelectionList(activeSelection, MFn.kMeshPolygonComponent)
    flattenObjectsInSelectionList(objectsWithSelectedFaces, strategy)

    print('flattening selection ... done')

def flattenObjectsInSelectionList(selectionListIter, strategy):
    while not selectionListIter.isDone():
        dagPath = MDagPath()
        components = MObject()
        selectionListIter.getDagPath(dagPath, components)
        print('flattening selection on object %(object)s' % {'object': dagPath.partialPathName()})

        connectedFaceSets = findConnectedFaces(dagPath, components)
        for connectedFaceSet in connectedFaceSets:
            if strategy is 'spiral':
                tree = createFacetreeSpiral(dagPath, connectedFaceSet)
            else:
                tree = createFacetreeLightning(dagPath, connectedFaceSet)
            patchBuilder = MeshPatchBuilder()
            flattenTree(dagPath, tree, patchBuilder)
        selectionListIter.next()
        print('flattening faces for selected object ... done')
