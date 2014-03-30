from unittest import TestCase
from unfolder.graph.test.sample_graphs import createSimpleGraph, createSimpleTree, createGraphWithIsolatedNode


class TestGraph(TestCase):

    def test_isTree_hasCycles(self):
        simpleGraph = createSimpleGraph()

        self.assertFalse(simpleGraph.isTree())

    def test_isTree_tree(self):
        simpleTree = createSimpleTree()

        self.assertTrue(simpleTree.isTree())

    def test_isTree_hasIsolatedNode(self):
        graph = createGraphWithIsolatedNode()

        self.assertFalse(graph.isTree())

    def test_getSpanningTree(self):
        simpleTree = createSimpleGraph()
        simpleTreeSpanningTree = simpleTree.getSpanningTree()

        self.assertTrue(simpleTreeSpanningTree.isTree())

        simpleGraph = createSimpleGraph()
        simpleGraphSpanningTree = simpleGraph.getSpanningTree()

        self.assertTrue(simpleGraphSpanningTree.isTree())

    def test_getSpanningTree_hasIsolatedNode(self):
        graph = createGraphWithIsolatedNode()

        self.assertRaises(ValueError, graph.getSpanningTree)
