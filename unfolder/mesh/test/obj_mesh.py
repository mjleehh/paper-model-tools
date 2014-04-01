from unittest import TestCase
from unfolder.mesh.obj_importer import ObjImporter
from unfolder.mesh.obj_mesh import ObjEdge, MeshFaces


class MeshFacesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        reader = ObjImporter()
        cls.mesh = reader.read('resources/pyramid.obj')

    def test_len(self):
        faces = MeshFaces(self.mesh)
        self.assertEqual(len(faces), 5)

    def test_contains(self):
        faces = MeshFaces(self.mesh)
        for i in range(5):
            self.assertTrue(i in faces)

        self.assertFalse(18 in faces)

    def test_getitem(self):
        faces = MeshFaces(self.mesh)
        for i, face in enumerate(faces):
            self.assertEqual(face.index, faces[i].index)

    def test_iter(self):
        faces = MeshFaces(self.mesh)
        for i, face in enumerate(faces):
            self.assertEqual(i, face.index)


class MeshFaceTest(TestCase):
    @classmethod
    def setUpClass(cls):
        reader = ObjImporter()
        mesh = reader.read('resources/pyramid.obj')
        cls.face = MeshFaces(mesh)[3]

    def test_getConnectedFaces(self):
        connectedFaces = self.face.getConnectedFaces()

        self.assertEqual(len(connectedFaces), 3)
        expectedConnectedFaceIndices = set([connectedFace.index for connectedFace in connectedFaces])
        self.assertEqual({0, 2, 4}, expectedConnectedFaceIndices)

    def test_getVertices(self):
        expectedFaceVertices = [(0.999997, -35.355339, 82.710678), (71.710678, -35.355339, 12.0), (1.0, 35.355339, 12.0)]
        self.assertEqual(expectedFaceVertices, self.face.getVertices())
