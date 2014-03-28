from .graph import Graph, GraphEdge


class GraphBuilder:
    def __init__(self):
        self._nodes = []
        self._edges = {}

    def addNode(self, value, connectedValues):
        self._createNode(value)
        for otherValue in self._findNewConnections(value, connectedValues):
            self._createNode(otherValue)
            self._createEdge(value, otherValue)


    # private

    def _findNewConnections(self, node, connectedValues):
        currentlyConnectedValues = frozenset(self._getConnectedNodes(node))
        return frozenset(connectedValues) - currentlyConnectedValues

    def _getConnectedNodes(self, node):
        return [edge.getOther(node) for edge in self._edges.values() if edge.hasNode(node)]

    def _createNode(self, value):
        if value not in self._nodes:
            self._nodes.append(value)

    def _createEdge(self, firstNode, secondNode):
        edge = GraphEdge(firstNode, secondNode)
        edgeKey = hash(edge)
        if edgeKey in self._edges:
            return self._edges[edgeKey]
        else:
            self._edges[edgeKey] = edge
            return edge

    def toGraph(self):
        return Graph(self._nodes, self._edges)
