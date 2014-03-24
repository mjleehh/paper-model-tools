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

    def getEdgeIndices(self):
        retval = om.MIntArray()
        self._getFaceIter(self.index).getEdges(retval)
        return retval

    def _getFaceIter(self, faceIndex):
        return setIter(om.MItMeshPolygon(), faceIndex)


def setIter(iter, index):
    prevIndex = om.MScriptUtil()
    prevIndex.createFromInt(0)
    iter.setIndex(index, prevIndex.asIntPtr())
    return iter