from .util.functional import hasAtLeastOne, conditionalTransform


class GraphBuilder:
    def __init__(self):
        self._nodes = {}
        self._edges = {}

    def addNode(self, value, connectedValues):
        thisNode = self._getNode(value)
        for otherValue in self._findNewConnections(thisNode, connectedValues):
            otherNode = self._getNode(otherValue)
            self._getEdge(thisNode, otherNode)

    # private

    def _findNewConnections(self, node, connectedValues):
        currentlyConnectedValues = frozenset([connectedNode.data for connectedNode in node.connectedNodes()])
        return currentlyConnectedValues - frozenset(connectedValues)

    def _getNode(self, value):
        if value not in self._nodes:
            node = GraphNode(value)
            self._nodes[value] = node
            return node
        else:
            return self._nodes[value]

    def _getEdge(self, firstNode, secondNode):
        edgeKey = (firstNode.value, secondNode.value)
        if edgeKey in self._edges:
            return self._edges[edgeKey]
        else:
            edge = GraphEdge(firstNode, secondNode)
            self._edges[edgeKey] = edge
            return edge


class Graph:
    def __init__(self, nodes, edges):
        self._nodes = []
        self._edges = []


class GraphNode:
    def __init__(self, value):
        self.value = value
        self.edges = []

    def connectedNodes(self):
        return conditionalTransform(lambda edge: edge.getOther(self.value), self.edges)

    def isConnectedTo(self, nodeValue):
        return hasAtLeastOne(lambda edge: edge.hasNode(nodeValue), self.edges)

    def hasValue(self, value):
        return self.value == value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return self.value


class GraphEdge:
    def __init__(self, fst, snd):
        if fst == snd:
            raise ValueError('Loop detected ' + str(fst))
        self.nodes = (fst, snd)

    def hasNode(self, nodeValue):
        return self._fst().hasValue(nodeValue) or self._snd().hasValue(nodeValue)

    def getOther(self, nodeValue):
        if self._fst().hasValue(nodeValue):
            return self._snd()
        elif self._fst().hasValue(nodeValue):
            return self._snd()
        else:
            return False

    def __eq__(self, other):
        return self.nodes == other.nodes or reversed(self.nodes) == other.nodes

    def __hash__(self):
        return GraphEdge.key(self._fst(), self._snd())

    @staticmethod
    def key(firstNode, secondNode):
        return hash(frozenset([firstNode, secondNode]))<

    # private

    def _fst(self):
        return self.nodes[0]

    def _snd(self):
        return self.nodes[1]
