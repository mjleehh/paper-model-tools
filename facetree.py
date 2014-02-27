from maya.OpenMaya import MItMeshPolygon, MIntArray
from helpers import setIter


class Node:
    """ Nodes of a face tree.

    A face tree structure, where each parent shares at least one edge with its siblings.
    """
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def sf(self, offset = 0):
        res = " " * offset + str(self.value) + '\n'
        for child in self.children:
            res += child.sf(offset + 1)
        return res


def createFacetreeLightning(dagPath, connectedFaces):
    """ Create a face tree by appending as many faces to a parent face as possible.
    """

    def createFaceIter(initialFace):
        retval = MItMeshPolygon(dagPath)
        setIter(retval, initialFace)
        return retval

    def extractConnectedFaces(faceIter, remainingFaces):
        face = faceIter.index()

        connectedFaces = MIntArray()
        faceIter.getConnectedFaces(connectedFaces)
        neighbours = frozenset(connectedFaces) & remainingFaces
        remainingFaces -= neighbours

        children = []
        for connectedFace in neighbours:
            setIter(faceIter, connectedFace)
            children.append(extractConnectedFaces(faceIter, remainingFaces))

        return Node(face, children)

    print("duplicating patch")
    initialFace = connectedFaces[0]
    remainingFaces = set(connectedFaces[1:])
    faceIter = createFaceIter(initialFace)
    tree = extractConnectedFaces(faceIter, remainingFaces)
    print("duplicating patch ... done")
    return tree


def createFacetreeSpiral(dagPath, connectedFaces):

    def createFaceIter(initialFace):
        faceIter = MItMeshPolygon(dagPath)
        setIter(faceIter, initialFace)
        return faceIter

    def traverseTreeStub(node, remainingFaces):
        if node.children:
            for child in node.children:
                traverseTreeStub(child, remainingFaces)
        else:
            addDirectChildren(node, remainingFaces)

    def addDirectChildren(node, remainingFaces):
        print(node.value)
        faceIter = createFaceIter(node.value)

        connectedFaces = MIntArray()
        faceIter.getConnectedFaces(connectedFaces)
        neighbours = frozenset(connectedFaces) & remainingFaces
        remainingFaces -= neighbours

        children = []
        for connectedFace in neighbours:
            children.append(Node(connectedFace, []))
        node.children = children

    print("duplicating patch")
    initialFace = connectedFaces[0]
    remainingFaces = set(connectedFaces[1:])
    tree = Node(initialFace, [])
    while remainingFaces:
        traverseTreeStub(tree, remainingFaces)
    print("duplicating patch ... done")
    return tree

