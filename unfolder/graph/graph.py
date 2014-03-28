class Graph:
    def __init__(self, nodes, edges):
        self._nodes = sorted(nodes)
        self._edges = edges

    def isConnected(self):
        return len(self._getConnectedNodes()) == 1

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

    def getConnectedNodes(self, node):
        return [edge.getOther(node) for edge in self._edges.values() if edge.hasNode(node)]

    def getConnectedEdges(self, node):
        return [edge for edge in self._edges.values() if edge.hasNode(node)]

    # private

    def _getConnectedNodes(self):

        def findConnectedGraph(remainingNodes):
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
        remainingNodes = set(self._nodes)
        while remainingNodes:
            connectedGraphs.append(findConnectedGraph(remainingNodes))
        return connectedGraphs


    def __repr__(self):
        retval = 'G = (\n  V = {'
        delim = ''
        for node in self._nodes:
            retval += delim + repr(node)
            delim = ', '
        retval += '},\n  E = {'
        delim = ''
        for edge in self._edges:
            retval += delim + repr(edge)
            delim = ', '
        retval += "}\n)"
        return retval


class GraphEdge:
    def __init__(self, fst, snd):
        if fst == snd:
            raise ValueError('Loop detected ' + str(fst))
        self.nodes = (fst, snd) if fst < snd else (snd, fst)

    def hasNode(self, node):
        return self._fst() == node or self._snd() == node

    def getOther(self, node):
        if self._fst() == node:
            return self._snd()
        elif self._snd() == node:
            return self._fst()
        else:
            return None

    def __hash__(self):
        return hash(self.nodes)

    def __repr__(self):
        return str(self.nodes)

    # private

    def _fst(self):
        return self.nodes[0]

    def _snd(self):
        return self.nodes[1]
