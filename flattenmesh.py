from maya.OpenMaya import MSelectionList, MItSelectionList, MDagPath, MObject, MFn, MGlobal

from connectedfaces import findConnectedFaces
from facetree import FaceTree
from patch import Patch


def flattenMesh():
    """ Unfold mesh selection.
    """
    print("flattening selection")

    activeSelection = MSelectionList()
    MGlobal.getActiveSelectionList(activeSelection)

    selectedObjects = MItSelectionList(activeSelection, MFn.kMesh)
    flattenObjectsInSelectionList(selectedObjects)

    objectsWithSelectedFaces = MItSelectionList(activeSelection, MFn.kMeshPolygonComponent)
    flattenObjectsInSelectionList(objectsWithSelectedFaces)

    print('flattening selection ... done')

def flattenObjectsInSelectionList(selectionListIter):
    while not selectionListIter.isDone():
        dagPath = MDagPath()
        components = MObject()
        selectionListIter.getDagPath(dagPath, components)
        print('flattening selection on object %(object)s' % {'object' : dagPath.partialPathName()})

        connectedFaceSets = findConnectedFaces(dagPath, components)
        for connectedFaceSet in connectedFaceSets:
            tree = FaceTree(connectedFaceSet, dagPath).getForCenter(0)
            Patch(dagPath).createForTree(tree)
        selectionListIter.next()
        print('flattening faces for selected object ... done')
