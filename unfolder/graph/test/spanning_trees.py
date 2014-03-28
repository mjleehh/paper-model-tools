from unittest import TestCase
from unfolder.graph.graph_builder import GraphBuilder
from unfolder.graph.spanning_trees import spanningTrees


class TestSpanningTrees(TestCase):
    def test_spanningTrees(self):
        graphBuilder = GraphBuilder()
        graphBuilder.addNode('A', ['B', 'D'])
        graphBuilder.addNode('B', ['A', 'C', 'D'])
        graphBuilder.addNode('C', ['B', 'D'])
        graphBuilder.addNode('D', ['A', 'B', 'C'])
        graph = graphBuilder.toGraph()

        for spanningTree in spanningTrees(graph):
            pass