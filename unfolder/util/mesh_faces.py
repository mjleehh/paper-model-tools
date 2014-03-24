import maya.OpenMaya as om

class MeshFaces:
    def __init__(self, dagPath, faceIndices):
        self._dagPath = dagPath
        self.faceIndices = faceIndices

    def __len__(self):
        return len(self.faceIndices)

    def __getitem__(self, faceIndex):
        if not self.__contains__(faceIndex):
            raise KeyError('Invalid face index ' + str(faceIndex))
        return MeshFace(self._dagPath, faceIndex)

    def __contains__(self, faceIndex):
        return faceIndex in self.faceIndices

    def __iter__(self):
        for faceIndex in self.faceIndices:
            yield self[faceIndex]

class MeshFace:
    def __init__(self, dagPath, index):
        self._dagPath = dagPath
        self.index = index

    def __len__(self):
        return self._getEdgeIndices().length()

    def getConnectingEdges(self, otherFace):
        sharedEdgeIndices = frozenset(self._getEdgeIndices()) & frozenset(otherFace._getEdgeIndices())
        return [MeshEdge(self._dagPath, index) for index in sharedEdgeIndices]

    def _getEdgeIndices(self):
        retval = om.MIntArray()
        self._getFaceIter().getEdges(retval)
        return retval

    def _getFaceIter(self):
        return setIter(om.MItMeshPolygon(), self.index)

class MeshEdge:
    def __init__(self, dagPath, index):
        self._dagPath = dagPath
        self.index = index

    def getConnectedFaces(self):
        return [MeshFace(self._dagPath, index) for index in self._getConnectedFaceIndices()]

    def _getConnectedFaceIndices(self):
        retval = om.MIntArray()
        self._getEdgeIter().getConnectedFaces(retval)
        return retval

    def _getEdgeIter(self):
        return setIter(om.MItMeshEdge, self.index)

def setIter(iter, index):
    prevIndex = om.MScriptUtil()
    prevIndex.createFromInt(0)
    iter.setIndex(index, prevIndex.asIntPtr())
    return iter