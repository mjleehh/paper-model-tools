import maya.OpenMaya as om


class MeshPatchBuilder:
    def __init__(self):
        self.mapping = []
        self._createMesh()

    def addFace(self, face, vertices):
        print('mapped ' + str(face) + ' -> ' + str(len(self.mapping)))
        self.mapping.append(face)
        self.mesh.addPolygon(vertices)

    def reset(self):
        om.MGlobal.removeFromModel(self.mesh.object())
        self.mapping = []
        self._createMesh()


    def _createMesh(self):
        self.mesh = om.MFnMesh()
        self.mesh.create(0, 0, om.MFloatPointArray(), om.MIntArray(), om.MIntArray())
        list = om.MSelectionList()
        list.add('initialShadingGroup')
        sg = om.MObject()
        list.getDependNode(0, sg)

        sgf = om.MFnSet(sg)
        sgf.addMember(self.mesh.object())