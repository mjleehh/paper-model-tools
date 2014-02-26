from maya.OpenMaya import MItMeshPolygon, MIntArray
from helpers import setIter


class Node:
    """ Nodes of a face tree.

    A face tree structure, where each parent shares at least one edge with its siblings.
    """
    def __init__(self, node, children):
        self.node = node
        self.children = children

    def sf(self, offset = 0):
        res = " " * offset + str(self.node) + '\n'
        for child in self.children:
            res += child.sf(offset + 1)
        return res


def createFacetree(dagPath, connectedFaces):
    """ Create a face tree by appending as many faces to a parent face as possible.
    """

    def createFaceIter(initialFace):
        faceIter = MItMeshPolygon(dagPath)
        setIter(faceIter, initialFace)
        return faceIter

    def extractConnectedFaces(faceIter, remainingFaces):
        face = faceIter.index()

        connectedFaces = MIntArray()
        faceIter.getConnectedFaces(connectedFaces)
        neighbours = set(connectedFaces) & remainingFaces
        remainingFaces -= neighbours

        children = []
        for connectedFace in neighbours:
            setIter(faceIter, connectedFace)
            children.append(extractConnectedFaces(faceIter, remainingFaces))

        return Node(face, children)

    print("duplicating patch")
    initialFace = connectedFaces[0]
    remainingFaces = set(connectedFaces)
    remainingFaces.remove(initialFace)
    faceIter = createFaceIter(initialFace)
    tree = extractConnectedFaces(faceIter, remainingFaces)
    print("duplicating patch ... done")
    return tree