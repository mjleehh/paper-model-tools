from unfolder.graph.graph import Graph
from unfolder.graph.graph_impl import EdgeImpl, GraphImpl


def buildGraph():
    return GraphBuilder()

class GraphBuilder:
    def __init__(self):
        self._nodes = []
        self._nodeMap = {}
        self._edgeLists = []
        self._edges = []
        self._edgeMap = {}

    def addNode(self, value, connectedValues):
        thisIndex = self._createNode(value)
        for otherValue in self._findNewConnections(thisIndex, connectedValues):
            otherIndex = self._createNode(otherValue)
            self._createEdge(thisIndex, otherIndex)
        return self

    # private

    def _findNewConnections(self, nodeIndex, connectedValues):
        currentlyConnectedValues = frozenset(self._getConnectedNodes(nodeIndex))
        return frozenset(connectedValues) - currentlyConnectedValues

    def _getConnectedEdges(self, nodeIndex):
        return [self._edges[edgeIndex] for edgeIndex in self._edgeLists[nodeIndex]]

    def _getConnectedNodes(self, nodeIndex):
        def getOther(edge, nodeIndex):
            nodes = edge.nodes
            return nodes[not nodes.index(nodeIndex)]
        return [getOther(edge, nodeIndex) for edge in self._getConnectedEdges(nodeIndex)]

    def _createNode(self, value):
        if value in self._nodeMap:
            return self._nodeMap[value]
        else:
            index = len(self._nodes)
            self._nodes.append(value)
            self._nodeMap[value] = index
            self._edgeLists.append([])
            return index

    def _createEdge(self, firstIndex, secondIndex):
        edge = EdgeImpl(firstIndex, secondIndex)
        if edge in self._edgeMap:
            return self._edgeMap[edge]
        else:
            index = len(self._edges)
            self._edges.append(edge)
            self._edgeMap[edge] = index
            self._edgeLists[firstIndex].append(index)
            self._edgeLists[secondIndex].append(index)
            return index

    def toGraph(self):
        return Graph(GraphImpl(self._nodes, self._edges))
