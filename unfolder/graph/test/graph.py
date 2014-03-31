from unittest import TestCase
from unfolder.graph.test.sample_graphs import createSimpleGraph, createSimpleTree, createGraphWithIsolatedNode, \
    createEmptyGraph, createPrimitiveGraph, createSingularGraph, \
    createDiamondGraph


class TestGraph(TestCase):

    def test_isTree_hasCycles(self):
        simpleGraph = createSimpleGraph()

        self.assertFalse(simpleGraph.isTree())

        diamondGraph = createDiamondGraph()

        self.assertFalse(diamondGraph.isTree())

    def test_isTree_empty(self):
        simpleTree = createEmptyGraph()

        self.assertTrue(simpleTree.isTree())

    def test_isTree_tree(self):
        singularGraph = createSingularGraph()

        self.assertTrue(singularGraph.isTree())

        primitiveGraph = createPrimitiveGraph()

        self.assertTrue(primitiveGraph.isTree())

        simpleTree = createSimpleTree()

        self.assertTrue(simpleTree.isTree())

    def test_isTree_hasIsolatedNode(self):
        graph = createGraphWithIsolatedNode()

        self.assertFalse(graph.isTree())

    def test_getSpanningTree_empty(self):
        emptyGraph = createEmptyGraph()
        emptyGraphGraphSpanningTree = emptyGraph.getSpanningTree()

        self.assertTrue(emptyGraphGraphSpanningTree.isTree())

    def test_getSpanningTree_oneElement(self):
        singularGraph = createSingularGraph()
        singularGraphSpanningTree = singularGraph.getSpanningTree()

        self.assertTrue(singularGraphSpanningTree.isTree())

    def test_getSpanningTree(self):
        primitiveGraph = createPrimitiveGraph()
        primitiveGraphSpanningTree = primitiveGraph.getSpanningTree()

        self.assertTrue(primitiveGraphSpanningTree.isTree())

        simpleTree = createSimpleGraph()
        simpleTreeSpanningTree = simpleTree.getSpanningTree()

        self.assertTrue(simpleTreeSpanningTree.isTree())

        simpleGraph = createSimpleGraph()
        simpleGraphSpanningTree = simpleGraph.getSpanningTree()

        self.assertTrue(simpleGraphSpanningTree.isTree())

        diamondGraph = createDiamondGraph()
        diamondGraphTree = diamondGraph.getSpanningTree()

        self.assertTrue(diamondGraphTree.isTree())

    def test_getSpanningTree_hasIsolatedNode(self):
        graph = createGraphWithIsolatedNode()

        self.assertRaises(ValueError, graph.getSpanningTree)

    def test_connectedComponents(self):
        simpleGraph = createSimpleGraph()
        simpleGraph.getConnectedComponents()

        twoComponentGraph = createGraphWithIsolatedNode()
        twoComponents = twoComponentGraph.getConnectedComponents()

        print(twoComponents)
