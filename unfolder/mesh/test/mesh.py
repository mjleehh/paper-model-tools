from unittest import TestCase
from unfolder.mesh.obj_importer import ObjImporter
from unfolder.mesh.mesh import Mesh


class MeshTests(TestCase):
    @classmethod
    def setUpClass(cls):
        reader = ObjImporter()
        cls.meshImpl = reader.read('resources/box.obj')

    def setUp(self):
        self.mesh = Mesh(self.meshImpl)

    def test_faces(self):
        faces = self.mesh.faces

        self.assertEquals(len(faces), 6)

    def test_edges(self):
        edges = self.mesh.edges

        self.assertEqual(len(edges), 12)

    def test_vertices(self):
        expectedVertices = [(-73.5, -61.25, 65.900002), (76.5, -61.25, 65.900002), (-73.5, 61.25, 65.900002), (76.5, 61.25, 65.900002), (-73.5, 61.25, -65.400002), (76.5, 61.25, -65.400002), (-73.5, -61.25, -65.400002), (76.5, -61.25, -65.400002)]

        vertices = self.mesh.vertices
        self.assertEqual(len(vertices), 8)
        for vertexIndex, vertex in enumerate(vertices):
            self.assertEqual(vertex, expectedVertices[vertexIndex])
