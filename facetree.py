from maya.OpenMaya import *

from helpers import *


class Node:
    def __init__(self, node, children):
        self.node = node
        self.children = children

    def sf(self, offset = 0):
        res = " " * offset + str(self.node) + '\n'
        for child in self.children:
            res += child.sf(offset + 1)
        return res


class FaceTree:
    def __init__(self, patch, dagPath):
        self._dagPath = dagPath
        self._patch = patch

    def getForCenter(self, initialFace):
        print("-- duplicating patch --")
        initialFace = self._patch[initialFace]
        remainingFaces = set(self._patch)
        remainingFaces.remove(initialFace)
        faceIter = self._createFaceIter(initialFace)
        tree = self._extractConnectedFaces(faceIter, remainingFaces)
        print("-- done --")
        return tree

    def _createFaceIter(self, initialFace):
        faceIter = MItMeshPolygon(self._dagPath)
        setIter(faceIter, initialFace)
        return faceIter

    def _extractConnectedFaces(self, faceIter, remainingFaces):
        face = faceIter.index()

        connectedFaces = MIntArray()
        faceIter.getConnectedFaces(connectedFaces)
        neighbours = set(connectedFaces) & remainingFaces
        remainingFaces -= neighbours

        children = []
        for connectedFace in neighbours:
            setIter(faceIter, connectedFace)
            children.append(self._extractConnectedFaces(faceIter, remainingFaces))

        return Node(face, children)