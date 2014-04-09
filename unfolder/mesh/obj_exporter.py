from unfolder.mesh.obj_mesh import Mesh


class ObjExporter:

    def __init__(self, filename):
        self.filename = filename
        self.f = None

    def write(self, mesh: Mesh):
        with open(self.filename, 'w') as self.f:
            for vertex in mesh.vertices:
                self.writeVertex(vertex)
            for face in mesh.faces:
                self.writeFace(face)

    def writeVertex(self, vertex):
        (x, y, z) = vertex
        self.f.write('v ')
        self.f.write(str(x) + ' ')
        self.f.write(str(y) + ' ')
        self.f.write(str(z) + '\n')

    def writeFace(self, face):
        self.f.write('f')
        for vertex in face.vertexIndices:
            self.f.write(' ' + str(vertex))
        self.f.write('\n')