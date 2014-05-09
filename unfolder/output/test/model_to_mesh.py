from unittest import TestCase
from unfolder.graph.graph_impl import GraphImpl, EdgeImpl
from unfolder.mesh.face import FaceIter
from unfolder.mesh.mesh import Mesh
from unfolder.mesh.obj_exporter import ObjExporter
from unfolder.mesh.obj_importer import ObjImporter
from unfolder.model.tree_to_model.tree_to_model import treeToModel
from unfolder.output.model_to_mesh import modelToMesh
from unfolder.tree.knot import graphToTree


class ModelToMeshTester(TestCase):
    def setUp(self):
        NODES = [1, 0, 2]
        EDGES = [(0, 1), (1, 2)]

        reader = ObjImporter()
        mesh = reader.read('resources/corner.obj')
        faces = FaceIter(mesh)

        graphEdges = [EdgeImpl(fst, snd) for fst, snd in EDGES]

        treeGraph = GraphImpl(NODES, graphEdges)
        tree = graphToTree(treeGraph)
        self.model = treeToModel(tree, faces)

    def test_patches(self):
        mesh = modelToMesh(self.model)
        writer = ObjExporter('tmp/junk.obj')
        writer.write(Mesh(mesh))