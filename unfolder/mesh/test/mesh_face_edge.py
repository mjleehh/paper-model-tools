from unittest import TestCase
from unfolder.mesh.obj_importer import ObjImporter
from unfolder.mesh.obj_mesh import MeshFaces


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
