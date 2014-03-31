class Graph:

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def isEmpty(self):
        return not self.nodes

    def numNodes(self):
        return len(self.nodes)

    def numEdges(self):
        return len(self.edges)

    def isConnected(self):
        return len(self.getConnectedComponents()) == 1

    def nodeIndex(self, node):
        return self.nodes.index(node)

    def edgeIndex(self, edge):
        return self.edges.index(edge)

    def clone(self):
        return Graph(self.nodes[:], self.edges[:])

    def isTree(self):
        return self.isEmpty() or self._traverse(TreeChecker())

    def getSpanningTree(self):
        if self.isEmpty():
            return Graph([], [])
        else:
            return self._traverse(SpanningTreeBuilder(self))

    def getConnectedComponents(self):
        retval = []
        remainingNodes = set(self.nodes)
        while remainingNodes:
            rootIndex = self.nodes.index(next(iter(remainingNodes)))
            graph = self._traverse(ConnectedComponentFinder(self), rootIndex)
            remainingNodes -= set(graph.nodes)
            retval.append(graph)
        return retval


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

    # private

    def _getConnectedNodeIndices(self, nodeIndex):
        return [edge.getOther(nodeIndex) for edge in self.edges if edge.hasNode(nodeIndex)]

    def _traverse(self, f, rootNodeIndex = 0):
        def traverseFromNode(nodeIndex, parentIndex):
            if visitedNodes[nodeIndex]:
                f.cycle(nodeIndex, parentIndex)
            else:
                visitedNodes[nodeIndex] = True
                f.newNode(nodeIndex, parentIndex)
                for connectedNodeIndex in self._getConnectedNodeIndices(nodeIndex):
                    if connectedNodeIndex != parentIndex:
                        traverseFromNode(connectedNodeIndex, nodeIndex)

        visitedNodes = [False] * len(self.nodes)
        try:
            traverseFromNode(rootNodeIndex, None)
            return f.done(visitedNodes)
        except StopGraphTraversal as s:
            return s.result


class StopGraphTraversal(Exception):
    def __init__(self, result):
        Exception.__init__(self)
        self.result = result


class GraphTraverser:
    def cycle(self, nodeIndex, parentIndex):
        pass

    def newNode(self, nodeIndex, parentIndex):
        pass

    def done(self, visitedNodes):
        pass


class TreeChecker(GraphTraverser):
    def cycle(self, nodeIndex, parentIndex):
        raise StopGraphTraversal(False)

    def done(self, visitedNodes):
        return all(visitedNodes)


class SpanningTreeBuilder(GraphTraverser):
    def __init__(self, graph):
        self._graph = graph
        self._edges = []

    def newNode(self, nodeIndex, parentIndex):
        if parentIndex is not None:
            self._edges.append(GraphEdge(parentIndex, nodeIndex))

    def done(self, visitedNodes):
        if len(self._edges) != self._graph.numNodes() - 1:
            raise ValueError('Error graph ' + repr(self._graph) + ' is not connected')
        return Graph(self._graph.nodes, self._edges)


class ConnectedComponentFinder(GraphTraverser):
    def __init__(self, graph):
        self._allNodes = graph.nodes
        self._nodes = []
        self._nodeMap = {}
        self._edges = []

    def cycle(self, nodeIndex, parentIndex):
        self._addEdge(nodeIndex, parentIndex)

    def newNode(self, nodeIndex, parentIndex):
        newIndex = len(self._nodes)
        self._nodes.append(self._allNodes[nodeIndex])
        self._nodeMap[nodeIndex] = newIndex
        if parentIndex is not None:
            self._addEdge(nodeIndex, parentIndex)

    def done(self, visitedNodes):
        return Graph(self._nodes, self._edges)

    def _addEdge(self, nodeIndex, parentIndex):
        newNodeIndex = self._nodeMap[nodeIndex]
        newParentIndex = self._nodeMap[parentIndex]
        self._edges.append(GraphEdge(newNodeIndex, newParentIndex))


class GraphEdge:
    def __init__(self, fstIndex, sndIndex):
        if fstIndex == sndIndex:
            raise ValueError('Loop detected ' + str(fstIndex))
        self.nodeIndices = (fstIndex, sndIndex) if fstIndex < sndIndex else (sndIndex, fstIndex)

    def hasNode(self, nodeIndex):
        return self.fst() == nodeIndex or self.snd() == nodeIndex

    def getOther(self, nodeIndex):
        if self.fst() == nodeIndex:
            return self.snd()
        elif self.snd() == nodeIndex:
            return self.fst()
        else:
            return None

    def __eq__(self, other):
        return self.nodeIndices == other.nodeIndices

    def __hash__(self):
        return hash(self.nodeIndices)

    def __repr__(self):
        return str(self.nodeIndices)

    def fst(self):
        return self.nodeIndices[0]

    def snd(self):
        return self.nodeIndices[1]
