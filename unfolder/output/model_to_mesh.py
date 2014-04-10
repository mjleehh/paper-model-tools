from unfolder.mesh.mesh_impl import FaceImpl
from unfolder.model.model_impl import Model


def modelToMesh(model: Model):
    meshBuilder = MeshBuilder()
    meshBuilder.vertices = model.vertices
    meshBuilder.edges = model.edges
    for patch in model.patches:
        meshBuilder.faces.append(FaceImpl(patch.edges, patch.textureCoords))


class MeshBuilder:
    def __init__(self):
        self.faces = []
        self.edges = []
        self.vertices = []
        self.textureCoords = []

