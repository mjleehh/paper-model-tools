from maya.OpenMaya import MItMeshPolygon, MIntArray
from helpers import setIter


def findConnectedFaces(dagPath, components):
    """ Given a mesh dag path and a subset of faces (optional) returns
    connected face groups.

    Connected faces share at least one edge. In a connected face group there
    is at least one path from every face to every other face in the group via
    a chain of connected faces.
    """

    def findPatch(remainingFaces):
        initialFace = iter(remainingFaces).next()
        faceIter = createFaceIter()
        setIter(faceIter, initialFace)
        res = addConnectedFaces(faceIter, remainingFaces)
        return res

    def createFaceIter():
        return MItMeshPolygon(dagPath, components)

    def getFaceList():
        faceIter = createFaceIter()
        facelist = []
        while not faceIter.isDone():
            facelist.append(faceIter.index())
            faceIter.next()
        return facelist

    def addConnectedFaces(faceIter, remainingFaces):
        face = faceIter.index()
        remainingFaces.remove(face)
        patch = [face]
        connectedFaces = MIntArray()
        faceIter.getConnectedFaces(connectedFaces)
        for connectedFace in connectedFaces:
            if connectedFace in remainingFaces:
                setIter(faceIter, connectedFace)
                patch.extend(addConnectedFaces(faceIter, remainingFaces))
        return patch

    print('finding sets of connected faces')
    patches = []
    remainingFaces = set(getFaceList())
    while len(remainingFaces) > 0:
        patches.append(findPatch(remainingFaces))
    print('finding sets of connected faces ... done')
    print('found %(numsets)i sets of connected faces' % {'numsets' : len(patches)})
    return patches