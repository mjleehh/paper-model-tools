from maya.OpenMaya import *

from connectedfaces import ConnectedFaces
from facetree import FaceTree
from patch import Patch


def iterf(copy = False):
    print("---- flattening selection ----")
    activeSelection = MSelectionList()
    om.MGlobal.getActiveSelectionList(activeSelection)
    selectedObjects = MItSelectionList(activeSelection, MFn.kMeshPolygonComponent)
    while not selectedObjects.isDone():
            print('---- flattening mesh faces ----')
            dagPath = MDagPath()
            components = MObject()
            selectedObjects.getDagPath(dagPath, components)

            connectedFaceSets = ConnectedFaces(dagPath, components).get()
            for connectedFaceSet in connectedFaceSets:
                tree = FaceTree(connectedFaceSet, dagPath).getForCenter(0)
                Patch(dagPath).createForTree(tree)
            selectedObjects.next()
    print("---- done ----")

class Mesh:
    def __init__(self, vertices, edges, polygons = None):
        self.polygons = polygons
        self.vertices = vertices
        self.edges = edges

    def __str__(self):
        return 'vertices: ' + str(self.vertices) + '\nedges: ' + str(self.edges) + '\npolygons: ' + str(self.polygons)

