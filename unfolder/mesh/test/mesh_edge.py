from unittest import TestCase
from unfolder.mesh.obj_importer import ObjImporter
from unfolder.mesh.obj_mesh import MeshFaces
from unfolder.util.vector import Vector


class MeshEdgeTests(TestCase):
    @classmethod
    def setUpClass(cls):
        reader = ObjImporter()
        mesh = reader.read('resources/box.obj')
        cls.meshFaceEdges = MeshFaces(mesh)[3].edges

    def test_getItem(self):
        e1 = self.meshFaceEdges[0]
        self.assertEqual((-73.5, -61.25, -65.400002), e1[0])
        self.assertEqual((76.5, -61.25, -65.400002), e1[1])

        e2 = self.meshFaceEdges[1]
        self.assertEqual((76.5, -61.25, 65.900002), e2[0])
        self.assertEqual((76.5, -61.25, -65.400002), e2[1])

        e3 = self.meshFaceEdges[2]
        self.assertEqual((-73.5, -61.25, 65.900002), e3[0])
        self.assertEqual((76.5, -61.25, 65.900002), e3[1])

        e4 = self.meshFaceEdges[3]
        self.assertEqual((-73.5, -61.25, 65.900002), e4[0])
        self.assertEqual((-73.5, -61.25, -65.400002), e4[1])

    def test_flipped(self):
        e1 = self.meshFaceEdges[0]
        self.assertTrue(e1.flipped)

        e2 = self.meshFaceEdges[1]
        self.assertFalse(e2.flipped)

        e3 = self.meshFaceEdges[2]
        self.assertFalse(e3.flipped)

        e4 = self.meshFaceEdges[3]
        self.assertTrue(e4.flipped)

    def test_direction(self):
        e1 = self.meshFaceEdges[0]
        self.assertEqual(e1.direction, Vector(-150.0, 0.0, 0.0))

        e2 = self.meshFaceEdges[1]
        self.assertEqual(e2.direction, Vector(0.0, 0.0, -131.300004))

        e3 = self.meshFaceEdges[2]
        self.assertEqual(e3.direction, Vector(150.0, 0.0, 0.0))

        e4 = self.meshFaceEdges[3]
        self.assertEqual(e4.direction, Vector(0.0, 0.0, 131.300004))

    def test_begin(self):
        e1 = self.meshFaceEdges[0]
        self.assertEqual((76.5, -61.25, -65.400002), e1.begin)

        e2 = self.meshFaceEdges[1]
        self.assertEqual((76.5, -61.25, 65.900002), e2.begin)

        e3 = self.meshFaceEdges[2]
        self.assertEqual((-73.5, -61.25, 65.900002), e3.begin)

        e4 = self.meshFaceEdges[3]
        self.assertEqual((-73.5, -61.25, -65.400002), e4.begin)

    def test_end(self):
        e1 = self.meshFaceEdges[0]
        self.assertEqual((-73.5, -61.25, -65.400002), e1.end)

        e2 = self.meshFaceEdges[1]
        self.assertEqual((76.5, -61.25, -65.400002), e2.end)

        e3 = self.meshFaceEdges[2]
        self.assertEqual((76.5, -61.25, 65.900002), e3.end)

        e4 = self.meshFaceEdges[3]
        self.assertEqual((-73.5, -61.25, 65.900002), e4.end)

    def test_hash_and_eq(self):
        for i, this in enumerate(self.meshFaceEdges):
            for j, other in enumerate(self.meshFaceEdges):
                areEqual = i == j
                self.assertEqual(this == other, areEqual)
                self.assertEqual(hash(this) == hash(other), areEqual)