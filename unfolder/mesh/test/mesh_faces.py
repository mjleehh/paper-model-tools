from unittest import TestCase
from unfolder.mesh.obj_importer import ObjImporter
from unfolder.mesh.obj_mesh import MeshFaces


class MeshFacesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        reader = ObjImporter()
        cls.mesh = reader.read('resources/pyramid.obj')

    def setUp(self):
        self.faces = MeshFaces(self.mesh)

    def test_len(self):
        self.assertEqual(len(self.faces), 5)

    def test_getitem(self):
        for i, face in enumerate(self.faces):
            self.assertEqual(face.index, self.faces[i].index)

    def test_iter(self):
        for i, face in enumerate(self.faces):
            self.assertEqual(i, face.index)
