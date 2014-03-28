from unittest import TestCase
from unfolder.graph.graph_builder import GraphBuilder
from unfolder.graph.test.sample_graphs import createSimpleGraph

__author__ = 'ml'


class TestGraphBuilder(TestCase):

    def test_addNode(self):
        graph = createSimpleGraph()
        self.assertEqual(sorted(graph.nodes), ['A', 'B', 'C', 'D'])
