from unittest import TestCase
from unfolder.mesh.face import FaceIter
from unfolder.mesh.obj_importer import ObjImporter
from unfolder.util.vector import Vector


class MeshEdgeTests(TestCase):
    @classmethod
    def setUpClass(cls):
        reader = ObjImporter()
        mesh = reader.read('resources/box.obj')
        cls.faceEdgeIter = FaceIter(mesh)[3].edges

    def test_getItem(self):
        e1 = self.faceEdgeIter[0]
        self.assertEqual((-73.5, -61.25, -65.400002), e1[0])
        self.assertEqual((76.5, -61.25, -65.400002), e1[1])

        e2 = self.faceEdgeIter[1]
        self.assertEqual((76.5, -61.25, 65.900002), e2[0])
        self.assertEqual((76.5, -61.25, -65.400002), e2[1])

        e3 = self.faceEdgeIter[2]
        self.assertEqual((-73.5, -61.25, 65.900002), e3[0])
        self.assertEqual((76.5, -61.25, 65.900002), e3[1])

        e4 = self.faceEdgeIter[3]
        self.assertEqual((-73.5, -61.25, 65.900002), e4[0])
        self.assertEqual((-73.5, -61.25, -65.400002), e4[1])

    def test_flipped(self):
        e1 = self.faceEdgeIter[0]
        self.assertTrue(e1._isFlipped())

        e2 = self.faceEdgeIter[1]
        self.assertFalse(e2._isFlipped())

        e3 = self.faceEdgeIter[2]
        self.assertFalse(e3._isFlipped())

        e4 = self.faceEdgeIter[3]
        self.assertTrue(e4._isFlipped())

    def test_direction(self):
        e1 = self.faceEdgeIter[0]
        self.assertEqual(e1.direction, Vector(-150.0, 0.0, 0.0))

        e2 = self.faceEdgeIter[1]
        self.assertEqual(e2.direction, Vector(0.0, 0.0, -131.300004))

        e3 = self.faceEdgeIter[2]
        self.assertEqual(e3.direction, Vector(150.0, 0.0, 0.0))

        e4 = self.faceEdgeIter[3]
        self.assertEqual(e4.direction, Vector(0.0, 0.0, 131.300004))

    def test_begin(self):
        e1 = self.faceEdgeIter[0]
        self.assertEqual((76.5, -61.25, -65.400002), e1.begin)

        e2 = self.faceEdgeIter[1]
        self.assertEqual((76.5, -61.25, 65.900002), e2.begin)

        e3 = self.faceEdgeIter[2]
        self.assertEqual((-73.5, -61.25, 65.900002), e3.begin)

        e4 = self.faceEdgeIter[3]
        self.assertEqual((-73.5, -61.25, -65.400002), e4.begin)

    def test_end(self):
        e1 = self.faceEdgeIter[0]
        self.assertEqual((-73.5, -61.25, -65.400002), e1.end)

        e2 = self.faceEdgeIter[1]
        self.assertEqual((76.5, -61.25, -65.400002), e2.end)

        e3 = self.faceEdgeIter[2]
        self.assertEqual((76.5, -61.25, 65.900002), e3.end)

        e4 = self.faceEdgeIter[3]
        self.assertEqual((-73.5, -61.25, 65.900002), e4.end)

    def test_hash_and_eq(self):
        for i, this in enumerate(self.faceEdgeIter):
            for j, other in enumerate(self.faceEdgeIter):
                areEqual = i == j
                self.assertEqual(this == other, areEqual)
                self.assertEqual(hash(this) == hash(other), areEqual)