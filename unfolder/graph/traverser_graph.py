from unfolder.graph.graph_impl import GraphImpl
from unfolder.graph.node import Node


class GraphAnalyzer:
    def cycle(self, node, parent):
        pass

    def newNode(self, node, parent):
        pass

    def done(self, visitedNodes):
        pass

    # private

    def _stop(self, result):
        raise  StopGraphTraversal(result)

def traverseGraph(traverser: GraphAnalyzer, graph: GraphImpl, rootNode=None):
    node = rootNode if rootNode is not None else Node(0, graph)
    return GraphWalker(traverser, graph).walk(node)


# private


class GraphWalker:
    def __init__(self, f, graph):
        self.f = f
        self.graph = graph
        self._visitedNodes = None

    def walk(self, rootNode):
        self._visitedNodes = [False] * len(self.graph.nodes)
        try:
            self._walkFromNode(rootNode, None)
            return self.f.done(self._visitedNodes)
        except StopGraphTraversal as s:
            return s.result

    def _walkFromNode(self, node, parent):
        if self._visitedNodes[node.index]:
            self.f.cycle(node, parent)
        else:
            self._visitedNodes[node.index] = True
            self.f.newNode(node, parent)
            for connectedNode in node.connectedNodes:
                if not parent or connectedNode != parent:
                    self._walkFromNode(connectedNode, node)


class StopGraphTraversal(Exception):
    def __init__(self, result):
        Exception.__init__(self)
        self.result = result
