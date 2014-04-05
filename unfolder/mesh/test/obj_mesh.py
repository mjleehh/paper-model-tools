from unittest import TestCase
from unfolder.mesh.obj_importer import ObjImporter
from unfolder.mesh.obj_mesh import ObjEdge, MeshFaces
from unfolder.util.vector import Vector


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


class MeshFaceTests(TestCase):
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

    def test_getNormal(self):
        normal = self.face.getNormal()


class MeshFaceEdgeTests(TestCase):
    @classmethod
    def setUpClass(cls):
        reader = ObjImporter()
        mesh = reader.read('resources/pyramid.obj')
        cls.meshFaceEdges = MeshFaces(mesh)[3].edges
        cls.expectedEdges = (1, 7, 6)

    def test_getitem(self):
        e1 = self.meshFaceEdges[0]
        self.assertEqual(e1.index, 1)
        print(e1.index)

        e2 = self.meshFaceEdges[1]
        self.assertEqual(e2.index, 7)

        e3 = self.meshFaceEdges[2]
        self.assertEqual(e3.index, 6)

    def test_iter(self):
        for i, faceEdge in enumerate(self.meshFaceEdges):
            self.assertEqual(faceEdge.index, self.expectedEdges[i])

    def test_len(self):
        self.assertEqual(len(self.meshFaceEdges), 3)


class MeshEdgeTests(TestCase):
    @classmethod
    def setUpClass(cls):
        reader = ObjImporter()
        mesh = reader.read('resources/box.obj')
        cls.meshFaceEdges = MeshFaces(mesh)[3].edges

    def test_getItem(self):
        e1 = self.meshFaceEdges[0]
        v1 = e1[0]
        self.assertEqual((-73.5, -61.25, -65.400002), v1)
        v2 = e1[1]
        self.assertEqual((76.5, -61.25, -65.400002), v2)

        e2 = self.meshFaceEdges[1]
        v3 = e2[0]
        self.assertEqual((76.5, -61.25, 65.900002), v3)
        v4 = e2[1]
        self.assertEqual((76.5, -61.25, -65.400002), v4)

    def test_direction(self):
        e1 = self.meshFaceEdges[0]
        self.assertEqual(e1.direction(), Vector(-150.0, 0.0, 0.0))
        e2 = self.meshFaceEdges[1]
        self.assertEqual(e2.direction(), Vector(0.0, 0.0, -131.300004))
        e3 = self.meshFaceEdges[2]
        self.assertEqual(e3.direction(), Vector(150.0, 0.0, 0.0))
        e4 = self.meshFaceEdges[3]
        self.assertEqual(e4.direction(), Vector(0.0, 0.0, 131.300004))