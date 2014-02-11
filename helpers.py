from maya.OpenMaya import MScriptUtil


def setIter(iter, index):
    prevIndex = MScriptUtil()
    prevIndex.createFromInt(0)
    iter.setIndex(index, prevIndex.asIntPtr())

def vprint(v):
    print(v[0], v[1], v[2])

def v2print(v):
    print(v[0], v[1])
