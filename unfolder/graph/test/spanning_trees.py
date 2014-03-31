from unittest import TestCase
from unfolder.graph.graph import GraphEdge
from unfolder.graph.graph_builder import GraphBuilder
from unfolder.graph.spanning_trees import SpanningTrees
from unfolder.graph.test.sample_graphs import createGraphWithTreeSpanningTrees, createSimpleGraph, \
    createSingularGraph, createPrimitiveGraph, createEmptyGraph, \
    createSimpleTree, createDiamondGraph


class TestSpanningTrees(TestCase):

    def test_spanningTrees(self):

        testCases = [
            (createEmptyGraph(), 1),
            (createSingularGraph(), 1),
            (createPrimitiveGraph(), 1),
            (createSimpleTree(), 1),
            (createGraphWithTreeSpanningTrees(), 3),
            (createSimpleGraph(), 8),
            (createDiamondGraph(), 16)]

        for testCase in testCases:
            (graph, numSpanningTrees) = testCase

            spanningTreeEdgeSets = [frozenset(spanningTree.edges) for spanningTree in SpanningTrees(graph)]

            # check for correct number of spanning trees
            self.assertEqual(len(spanningTreeEdgeSets), numSpanningTrees)

            # check there are no spanning tree duplicates
            self.assertEqual(len(set(spanningTreeEdgeSets)), numSpanningTrees)

