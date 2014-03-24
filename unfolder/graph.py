from .util.functional import hasAtLeastOne, conditionalTransform


class GraphBuilder:
    def __init__(self):
        self._nodes = {}

    def addNode(self, data, connectedNodes):
        node = self._nodes[data] if data in self._nodes else GraphNode(data)
        currentlyConnectedNodes = [connectedNode.data for connectedNode in node.connectedNodes()]
        nodesToConnect = connectedNodes - currentlyConnectedNodes
        for nodeToConnectValue in nodesToConnect:
            nodeToConnect = self._nodes[nodeToConnectValue] if nodeToConnectValue in self._nodes else GraphNode(nodeToConnectValue)
            node.edges.append(GraphEdge(None, (node, nodeToConnect)))


class Graph:
    def __init__(self):
        self._nodes = []
        self._edges = []


class GraphNode:
    def __init__(self, data):
        self.data = data
        self.edges = []

    def connectedNodes(self):
        return conditionalTransform(lambda edge: edge.getOther(self.data))

    def isConnectedTo(self, nodeData):
        return hasAtLeastOne(lambda edge: edge.hasNode(nodeData), self.edges)

    def isData(self, nodeData):
        return self.data == nodeData

    def __eq__(self, other):
        return self.data == other.data


class GraphEdge:
    def __init__(self, edgeData, nodes):
        self._data = edgeData
        (self._fst, self._snd) = nodes

    def hasNode(self, nodeData):
        return self._fst.isData(nodeData) or self._snd.isData(nodeData)

    def isTerminus(self):
        return bool(self._snd)

    def getOther(self, nodeData):
        if self.isTerminus():
            return False
        if self._fst.isData(nodeData):
            return self._snd
        elif self._snd.isData(nodeData):
            return self._fst
        else:
            return False
