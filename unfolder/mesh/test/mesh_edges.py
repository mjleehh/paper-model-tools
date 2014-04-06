from unittest import TestCase
from unfolder.mesh.obj_importer import ObjImporter
from unfolder.mesh.obj_mesh import MeshEdges


class MeshEdgesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        reader = ObjImporter()
        cls.mesh = reader.read('resources/pyramid.obj')

    def setUp(self):
        self.edges = MeshEdges(self.mesh)

    def test_len(self):
        self.assertEqual(len(self.edges), 8)

    def test_getitem(self):
        for edgeIndex, edge in enumerate(self.edges):
