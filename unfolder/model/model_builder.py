import maya.OpenMaya as om


class MeshPatchBuilder:
    def __init__(self):
        self.mapping = []
        self.mesh = createMesh()

    def addFace(self, face, vertices):
        self.mapping.append(face)
        self.mesh.addPolygon(vertices)

    def reset(self):
        om.MGlobal.removeFromModel(self.mesh.object())
        self.mapping = []
        self.mesh = createMesh()


def createMesh():
    mesh = om.MFnMesh()
    mesh.create(0, 0, om.MFloatPointArray(), om.MIntArray(), om.MIntArray())
    list = om.MSelectionList()
    list.add('initialShadingGroup')
    sg = om.MObject()
    list.getDependNode(0, sg)

    sgf = om.MFnSet(sg)
    sgf.addMember(mesh.object())
    return mesh