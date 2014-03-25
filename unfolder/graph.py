def values(nodeList):
    return [node.value for node in nodeList]


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
        currentlyConnectedValues = frozenset(values(node.connectedNodes()))
        return currentlyConnectedValues - frozenset(connectedValues)

    def _getNode(self, value):
        if value not in self._nodes:
            node = GraphNode(value)
            self._nodes[value] = node
            return node
        else:
            return self._nodes[value]

    def _getEdge(self, firstNode, secondNode):
        edge = GraphEdge(firstNode, secondNode)
        edgeKey = hash(edge)
        if edgeKey in self._edges:
            return self._edges[edgeKey]
        else:
            self._edges[edgeKey] = edge
            return edge

    def toGraph(self):
        return Graph(self._nodes, self._edges)


class Graph:
    def __init__(self, nodes, edges):
        self._nodes = nodes
        self._edges = edges

    def getConnectedSubgraphs(self):

        def findConnectedGraph(remainingNodes):
            initialNode = iter(remainingNodes).next()
            res = addConnectedNodes(initialNode, remainingNodes)
            return res

        def addConnectedNodes(node, remainingNodes):
            remainingNodes.remove(node)
            subgraph = [node]
            connectedNodes = frozenset(node.getConnected()) - remainingNodes
            for connectedNode in connectedNodes:
                subgraph.extend(addConnectedNodes(connectedNode, remainingNodes))
            return subgraph

        connectedGraphs = []
        remainingNodes = set(self._nodes)
        while remainingNodes:
            connectedGraphs.append(findConnectedGraph(remainingNodes))
        return connectedGraphs


class GraphNode:
    def __init__(self, value):
        self.value = value
        self.edges = []

    def getConnectedNodes(self):
        return [edge.getOther(self) for edge in self.edges]


    #def isConnectedTo(self, nodeValue):
    #    return hasAtLeastOne(lambda edge: edge.hasNode(nodeValue), self.edges)

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)


class GraphEdge:
    def __init__(self, fst, snd):
        if fst == snd:
            raise ValueError('Loop detected ' + str(fst))
        self.nodes = (fst, snd)

    def hasNode(self, node):
        return self._fst() == node or self._snd() == node

    def getOther(self, node):
        if self._fst() == node:
            return self._snd()
        elif self._fst() == node:
            return self._snd()
        else:
            return None

    def __hash__(self):
        return hash(frozenset((self._fst(), self._snd())))

    # private

    def _fst(self):
        return self.nodes[0]

    def _snd(self):
        return self.nodes[1]
