from unfolder.model.model import Model


def modelToMesh(model: Model):
    meshBuilder = MeshBuilder()
    meshBuilder.vertices = model.impl.vertices
    meshBuilder.edges = model.impl.edges
    for patch in model.patches:
        edges = patch.patchEdges
        #meshBuilder.faces.append(FaceImpl(patch.edges, patch.textureCoords))
        print('patcheeee')


class MeshBuilder:
    def __init__(self):
        self.faces = []
        self.edges = []
        self.vertices = []
        self.textureCoords = []

