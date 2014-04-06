from unittest import TestCase
from unfolder.mesh.obj_importer import ObjImporter
from unfolder.mesh.obj_mesh_impl import ObjEdge


class ObjImporterTests(TestCase):

    def test_importObj_box(self):
        reader = ObjImporter()
        box = reader.read('resources/box.obj')

        # check if vertices have been imported correctly

        expectedVertices = [(-73.5, -61.25, 65.900002), (76.5, -61.25, 65.900002), (-73.5, 61.25, 65.900002), (76.5, 61.25, 65.900002), (-73.5, 61.25, -65.400002), (76.5, 61.25, -65.400002), (-73.5, -61.25, -65.400002), (76.5, -61.25, -65.400002)]
        self.assertEqual(box.vertices, expectedVertices)

        # texture coordinates are missing

        expectedTextureCoordinates = [(0.375, 0.0), (0.625, 0.0), (0.375, 0.25), (0.625, 0.25), (0.375, 0.5), (0.625, 0.5), (0.375, 0.75), (0.625, 0.75), (0.375, 1.0), (0.625, 1.0), (0.875, 0.0), (0.875, 0.25), (0.125, 0.0), (0.125, 0.25)]
        self.assertEqual(box.textureCoords, expectedTextureCoordinates)

        # check if faces have been imported correctly

        self.assertEqual(len(box.faces), 6)
        expectedFaceEdgeLists = [[0, 1, 2, 3], [2, 4, 5, 6], [5, 7, 8, 9], [8, 10, 0, 11], [10, 7, 4, 1], [11, 3, 6, 9]]
        expectedFaceTextureCoordList = [[0, 1, 3, 2], [2, 3, 5, 4], [4, 5, 7, 6], [6, 7, 9, 8], [1, 10, 11, 3], [12, 0, 2, 13]]
        for faceIndex, face in enumerate(box.faces):
            self.assertEqual(face.edges, expectedFaceEdgeLists[faceIndex])
            self.assertEqual(face.textureCoords, expectedFaceTextureCoordList[faceIndex])
        # check if edges have been imported correctly

        self.assertEqual(len(box.edges), 12)
        edgeTuples = [(0, 1), (1, 3), (2, 3), (0, 2), (3, 5), (4, 5), (2, 4), (5, 7), (6, 7), (4, 6), (1, 7), (0, 6)]
        expectedEdges = [ObjEdge(fst, snd) for (fst, snd) in edgeTuples]
        self.assertEqual(box.edges, expectedEdges)
