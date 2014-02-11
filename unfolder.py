from maya.OpenMaya import MSelectionList, MItSelectionList, MDagPath, MObject, MFn, MGlobal

from connectedfaces import ConnectedFaces
from facetree import FaceTree
from patch import Patch


def flatten_mesh():
    """ Unfold all selected faces.

    """
    print("flattening selection")

    activeSelection = MSelectionList()
    MGlobal.getActiveSelectionList(activeSelection)
    selectedObjects = MItSelectionList(activeSelection, MFn.kMeshPolygonComponent)
    while not selectedObjects.isDone():
        print('flattening faces for selected object')
        dagPath = MDagPath()
        components = MObject()
        selectedObjects.getDagPath(dagPath, components)

        connectedFaceSets = ConnectedFaces(dagPath, components).get()
        for connectedFaceSet in connectedFaceSets:
            tree = FaceTree(connectedFaceSet, dagPath).getForCenter(0)
            Patch(dagPath).createForTree(tree)
        selectedObjects.next()
        print('flattening faces for selected object ... done')

    print('flattening selection ... done')
