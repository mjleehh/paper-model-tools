import maya.OpenMaya as om

class MeshPatchBuilder:
    def __init__(self):
        self.mapping = []
        self.mesh = None

    def addFace(self, face, vertices):
        if not self.mesh:
            self.mesh = om.MFnMesh()

        print('mapped ' + str(face) + ' -> ' + str(len(self.mapping)))
        self.mapping.append(face)
        self.mesh.addPolygon(vertices)

    def reset(self):
        self.mapping = []
        if self.mesh:
            om.MGlobal.removeFromModel(self.mesh.object())
            self.mesh = None
