from unfolder.mesh.edge import EdgeIter
from unfolder.mesh.face import FaceIter
from unfolder.mesh.mesh_impl import MeshImpl


class Mesh:
    def __init__(self, impl: MeshImpl):
        self.impl = impl

    @property
    def faces(self):
        return FaceIter(self.impl)

    @property
    def edges(self):
        return EdgeIter(self.impl)

    @property
    def vertices(self):
        return self.impl.vertices









