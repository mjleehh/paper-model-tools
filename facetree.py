from maya.OpenMaya import MItMeshPolygon, MIntArray
from helpers import setIter

class Node:
    """ Nodes of a face tree.

    A face tree structure, where each sibling face only shares one edge with its parent.
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
    """ Create a face tree with depth first strategy
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
    """ Create a face tree with maximum children per parent node strategy
    """

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

def createFacetreeSelectionOrder(dagPath, orderedSelectedFaces):

    def createFaceIter(initialFace):
        faceIter = MItMeshPolygon(dagPath)
        setIter(faceIter, initialFace)
        return faceIter

    def addFaceStripToNode(node, remainingFaces):
            print(node.value)
            faceIter = createFaceIter(node.value)

            connectedFaces = MIntArray()
            faceIter.getConnectedFaces(connectedFaces)
            newFace = remainingFaces[0]
            if newFace in frozenset(connectedFaces):
                del remainingFaces[0]
                newNode = Node(newFace, [])
                node.children.append(newNode)
                if remainingFaces:
                    addNextFaceStripToSubtree(newNode, remainingFaces)
                return True

    def addNextFaceStripToSubtree(node, remainingFaces):
        if addFaceStripToNode(node, remainingFaces):
            return True
        else:
            for child in node.children:
                if addNextFaceStripToSubtree(child, remainingFaces):
                    return True
        return False

    print("duplicating patch")
    initialFace = orderedSelectedFaces[0]
    remainingFaces = orderedSelectedFaces[1:]
    tree = Node(initialFace, [])
    while remainingFaces:
        addNextFaceStripToSubtree(tree, remainingFaces)
    print("duplicating patch ... done")
    return tree