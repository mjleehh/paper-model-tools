from unfolder.mesh.mesh_impl import FaceImpl, MeshImpl
from unfolder.model.model import Model


def modelToMesh(model: Model):
    vertices = model.impl.vertices
    edges = model.impl.edges
    faces = []
    for patch in model.patches:
        faces.append(FaceImpl(patch.edges, None))
    return MeshImpl(faces, edges, vertices, None)
