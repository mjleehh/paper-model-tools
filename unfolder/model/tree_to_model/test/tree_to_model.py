from unittest import TestCase
from unfolder.graph.graph_impl import GraphImpl, EdgeImpl
from unfolder.mesh.face import FaceIter
from unfolder.mesh.obj_importer import ObjImporter
from unfolder.model.tree_to_model.tree_to_model import treeToModel
from unfolder.tree.knot import graphToTree


class TreeToModelTester:
    def setUp(self):
        """
                 +-------------+
                   .    1    . |
                      .   .    |
                        +   2  |
                      .   .    |
                   .    3    . |
                 +------------ +
               . |             |
            .    |             |
          +   4  |     0       |
            .    |             |
               . |             |
                 +-------------+
        """
        reader = ObjImporter()
        mesh = reader.read(self.OBJ_FILE_NAME)
        self.faces = FaceIter(mesh)

        graphEdges = [EdgeImpl(fst, snd) for fst, snd in self.EDGES]

        treeGraph = GraphImpl(self.NODES, graphEdges)
        self.tree = graphToTree(treeGraph)

    def test_patches(self):
        model = treeToModel(self.tree, self.faces)
        print(model.impl.edges)
        print(model.impl.vertices)
        for patch in model.patches:
            print(patch.name)
            print(patch.edges)
            print(patch.vertices)
            print('---------')


class PyramidToModelTests(TreeToModelTester, TestCase):
    OBJ_FILE_NAME = 'resources/pyramid.obj'
    NODES = [0, 1, 2, 3, 4]
    EDGES = [(4, 0), (0, 3), (3, 2), (2, 1)]


class CornerToModelTests(TreeToModelTester, TestCase):
    OBJ_FILE_NAME = 'resources/corner.obj'
    NODES = [1, 0, 2]
    EDGES = [(0, 1), (1, 2)]


class BoxToModelTests(TreeToModelTester, TestCase):
    OBJ_FILE_NAME = 'resources/box.obj'
    NODES = [0, 1, 2, 3, 4, 5]
    EDGES = ((0, 1), (0, 3), (3, 2), (3, 4), (2, 5))
