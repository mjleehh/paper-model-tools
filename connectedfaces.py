from maya.OpenMaya import MItMeshPolygon, MIntArray
from helpers import setIter


class ConnectedFaces:
    def __init__(self, dagPath, components):
        self._dagPath = dagPath
        self._components = components

    def get(self):
        print('finding sets of connected faces')
        patches = []
        remainingFaces = set(self._getFaceList())
        while len(remainingFaces) > 0:
            patches.append(self._findPatch(remainingFaces))
        print('finding sets of connected faces ... done')
        print('found %(numsets)i sets of connected faces' % {'numsets' : len(patches)})
        return patches

    def _findPatch(self, remainingFaces):
        initialFace = iter(remainingFaces).next()
        faceIter = self._createFaceIter()
        setIter(faceIter, initialFace)
        res = self._addConnectedFaces(faceIter, remainingFaces)
        return res

    def _createFaceIter(self):
        return MItMeshPolygon(self._dagPath, self._components)

    def _getFaceList(self):
        faceIter = self._createFaceIter()
        facelist = []
        while not faceIter.isDone():
            facelist.append(faceIter.index())
            faceIter.next()
        return facelist

    def _addConnectedFaces(self, faceIter, remainingFaces):
        face = faceIter.index()
        remainingFaces.remove(face)
        patch = [face]
        connectedFaces = MIntArray()
        faceIter.getConnectedFaces(connectedFaces)
        for connectedFace in connectedFaces:
            if connectedFace in remainingFaces:
                setIter(faceIter, connectedFace)
                patch.extend(self._addConnectedFaces(faceIter, remainingFaces))
        return patch
