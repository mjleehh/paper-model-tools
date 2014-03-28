class Graph:

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges


    def isConnected(self):
        return len(self._getConnectedNodes()) == 1

    def nodeIndex(self, node):
        return self.nodes.index(node)

    def edgeIndex(self, edge):
        return self.edges.index(edge)

    def getConnectedSubgraphs(self):
        retval = []
        subgraphsNodes = self._getConnectedNodes()
        for subgraphNodes in subgraphsNodes:
            nodes = []
            edges = {}
            for node in subgraphNodes:
                nodes.append(node)
                for edge in self.getConnectedEdges(node):
                    edges[edge] = edge
            retval.append(Graph(nodes, edges))
        return retval

    # private

    def _getConnectedNodeIndices(self, nodeIndex):
        return [edge.getOther(nodeIndex) for edge in self.edges if edge.hasNode(nodeIndex)]

    def _getConnectedNodes(self):

        def findConnectsedGraph(remainingNodes):
            initialNode = next(iter(remainingNodes))
            res = addConnectedNodes(initialNode, remainingNodes)
            return res

        def addConnectedNodes(node, remainingNodes):
            if node in remainingNodes:
                remainingNodes.remove(node)
                subgraph = [node]
                connectedNodes = frozenset(self.getConnectedNodes(node))
                unknownNodes = connectedNodes & remainingNodes
                for unknownNode in unknownNodes:
                    subgraph.extend(addConnectedNodes(unknownNode, remainingNodes))
                return subgraph
            else:
                return []

        connectedGraphs = []
        remainingNodes = set(self.nodes)
        while remainingNodes:
            connectedGraphs.append(findConnectedGraph(remainingNodes))
        return connectedGraphs

    def isTree(self):
        def traverse(nodeIndex, parentIndex):
            if visitedNodes[nodeIndex]:
                return True

            visitedNodes[nodeIndex] = True
            for connectedNodeIndex in self._getConnectedNodeIndices(nodeIndex):
                if connectedNodeIndex != parentIndex:
                    if traverse(connectedNodeIndex, nodeIndex):
                        return True

            return False

        visitedNodes = [False] * len(self.nodes)
        if traverse(0, None):
            return False

        for visitedNode in visitedNodes:
            if not visitedNode:
                return False

        return True


    def getSpanningTree(self, rootNodeIndex = 0):

        def traverse(nodeIndex, parentIndex):
            if notVisitedNodes[nodeIndex]:
                notVisitedNodes[nodeIndex] = False
                if parentIndex is not None:
                    edges.append(GraphEdge(parentIndex, nodeIndex))
                for connectedNodeIndex in self._getConnectedNodeIndices(nodeIndex):
                    if connectedNodeIndex != parentIndex:
                        traverse(connectedNodeIndex, nodeIndex)

        edges = []
        notVisitedNodes = [True] * len(self.nodes)
        traverse(rootNodeIndex, None)
        if len(edges) != len(self.nodes) - 1:
            raise ValueError('graph is not connected!')
        return Graph(self.nodes, edges)

    def __repr__(self):
        retval = 'G = (\n  V = {'
        delim = ''
        for node in self.nodes:
            retval += delim + repr(node)
            delim = ', '
        retval += '},\n  E = {'
        delim = ''
        for edge in self.edges:
            retval += delim + repr(edge)
            delim = ', '
        retval += "}\n)"
        return retval


class GraphEdge:
    def __init__(self, fstIndex, sndIndex):
        if fstIndex == sndIndex:
            raise ValueError('Loop detected ' + str(fstIndex))
        self.nodeIndices = (fstIndex, sndIndex) if fstIndex < sndIndex else (sndIndex, fstIndex)

    def hasNode(self, nodeIndex):
        return self._fst() == nodeIndex or self._snd() == nodeIndex

    def getOther(self, nodeIndex):
        if self._fst() == nodeIndex:
            return self._snd()
        elif self._snd() == nodeIndex:
            return self._fst()
        else:
            return None

    def __hash__(self):
        return hash(self.nodeIndices)

    def __repr__(self):
        return str(self.nodeIndices)

    # private

    def _fst(self):
        return self.nodeIndices[0]

    def _snd(self):
        return self.nodeIndices[1]
