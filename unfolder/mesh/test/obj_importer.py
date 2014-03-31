from unittest import TestCase
from unfolder.automatic_unfold.graph_from_maya_mesh import graphFromFaces
from unfolder.graph.graph_builder import GraphBuilder
from unfolder.mesh.obj_importer import ObjImporter
from unfolder.mesh.obj_mesh import MeshFaces


class TestGraph(TestCase):

    def test_testObjImport(self):
        reader = ObjImporter()
        mesh = reader.read('resources/box-and-pyramid.obj')

        graph = graphFromFaces(MeshFaces(mesh), GraphBuilder())
        self.assertFalse(graph.isConnected())
        subgraphs = graph.getConnectedComponents()

        print(len(subgraphs))
        print(subgraphs)

        for subgraph in subgraphs:
            self.assertTrue(subgraph.isConnected())
