from unfolder.graph.edge import EdgeIter
from unfolder.graph.graph_impl import GraphImpl, EdgeImpl
from unfolder.graph.traverser_graph import traverseGraph, GraphAnalyzer
from unfolder.graph.node import Node


class Graph:
    def __init__(self, impl: GraphImpl):
        self.impl = impl

    @property
    def edges(self):
        return EdgeIter(self.impl)

    @property
    def nodes(self):
        return self.impl.nodes

    def copy(self):
        return Graph(GraphImpl(self.impl.nodes[:], self.impl.edges[:]))

    def isEmpty(self):
        return not self.impl.nodes

    def isConnected(self):
        return len(self.getConnectedComponents()) == 1

    def isTree(self):
        return self.isEmpty() or traverseGraph(TreeChecker(), self.impl)

    def getSpanningTree(self):
        if self.isEmpty():
            return Graph(GraphImpl([], []))
        else:
            return traverseGraph(SpanningTreeBuilder(self), self.impl)

    def getConnectedComponents(self):
        retval = []
        remainingNodes = set(self.impl.nodes)
        while remainingNodes:
            rootIndex = self.impl.nodes.index(next(iter(remainingNodes)))
            graph = traverseGraph(ConnectedComponentFinder(self), self.impl, Node(rootIndex, self.impl))
            remainingNodes -= set(graph.impl.nodes)
            retval.append(graph)
        return retval


# private


class TreeChecker(GraphAnalyzer):
    def cycle(self, node, parent):
        self._stop(False)

    def done(self, visitedNodes):
        return all(visitedNodes)


class SpanningTreeBuilder(GraphAnalyzer):
    def __init__(self, graph):
        self._graph = graph
        self._edges = []

    def newNode(self, node, parent):
        if parent is not None:
            self._edges.append(EdgeImpl(parent.index, node.index))

    def done(self, visitedNodes):
        if len(self._edges) != len(self._graph.nodes) - 1:
            raise ValueError('Error graph ' + repr(self._graph) + ' is not connected')
        return Graph(GraphImpl(self._graph.nodes, self._edges))


class ConnectedComponentFinder(GraphAnalyzer):
    def __init__(self, graph):
        self._allNodes = graph.impl.nodes
        self._nodes = []
        self._nodeMap = {}
        self._edges = []

    def cycle(self, node, parent):
        self._addEdge(node, parent)

    def newNode(self, node, parent):
        newIndex = len(self._nodes)
        self._nodes.append(self._allNodes[node.index])
        self._nodeMap[node.index] = newIndex
        if parent is not None:
            self._addEdge(node, parent)

    def done(self, visitedNodes):
        return Graph(GraphImpl(self._nodes, self._edges))

    def _addEdge(self, node, parent):
        newNodeIndex = self._nodeMap[node.index]
        newParentIndex = self._nodeMap[parent.index]
        self._edges.append(EdgeImpl(newNodeIndex, newParentIndex))
