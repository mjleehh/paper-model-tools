from unfolder.graph.graph import Graph
from unfolder.graph.node import Node


def graphToTree(graph):
    return Knot(Node(0, graph), None)


class Knot:
    def __init__(self, node: Node, parent=None):
        self.node = node
        self._parent = parent
        self._children = node.connectedNodes.indices[:]
        if self._parent is not None:
            self._children.remove(parent.index)

    def __iter__(self):
        """ Iterate the children of the node. """
        for child in self._children:
            yield Knot(Node(child, self.node.graphImpl), self.node)

    @property
    def value(self):
        return self.node.value

    def getNames(self):
        ret = [self.value]
        for child in self:
            ret += child.getNames()
        return ret
