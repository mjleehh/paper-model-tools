from unittest import TestCase
from unfolder.mesh.obj_importer import ObjImporter
from unfolder.mesh.obj_mesh import MeshFaces


class MeshFaceTests(TestCase):
    @classmethod
    def setUpClass(cls):
        reader = ObjImporter()
        mesh = reader.read('resources/pyramid.obj')
        cls.faces = MeshFaces(mesh)

    def test_getConnectingEdges(self):
        f = self.faces[1]

        fc0v3 = self.faces[0]
        e = f.getConnectingEdges(fc0v3)
        fc2v4 = self.faces[2]
        fc4v5 = self.faces[4]
        fnc3 = self.faces[3]

    def test_getConnectedFaces(self):
        cfs1 = self.faces[0].getConnectedFaces()
        self._compareFaceSet(cfs1, 1, 2, 3, 4)

        cfs2 = self.faces[1].getConnectedFaces()
        self._compareFaceSet(cfs2, 0, 2, 4)

        cfs3 = self.faces[2].getConnectedFaces()
        self._compareFaceSet(cfs3, 0, 1, 3)

        cfs4 = self.faces[3].getConnectedFaces()
        self._compareFaceSet(cfs4, 0, 2, 4)

        cfs5 = self.faces[4].getConnectedFaces()
        self._compareFaceSet(cfs5, 0, 1, 3)

    def test_getVertices(self):
        expectedFaceVertices = [(0.999997, -35.355339, 82.710678), (71.710678, -35.355339, 12.0), (1.0, 35.355339, 12.0)]
        self.assertEqual(expectedFaceVertices, self.faces[3].getVertices())

    def test_getNormal(self):
        normal = self.faces[3].getNormal()
        print(normal)
        normal = self.faces[0].getNormal()
        print(normal)

    def test_eq_and_hash(self):
        for i, this in enumerate(self.faces):
            for j, other in enumerate(self.faces):
                areEqual = i == j
                self.assertEqual(this == other, areEqual)
                self.assertEqual(hash(this) == hash(other), areEqual)

    # private

    def _compareFaceSet(self, xs, *expected):
        indexSet = set([x.index for x in xs])
        self.assertEqual(indexSet, set(expected))
