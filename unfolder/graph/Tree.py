from unfolder.graph.graph import Graph

def graphToTree(graph):
    return Node(0, graph)


class Node:
    def __init__(self, index, graph: Graph, parent=None):
        self._graph = graph
        self._parent = parent
        self.index = index
        self._children = self._graph._getConnectedNodeIndices(index)
        if self._parent is not None:
            self._children.remove(parent)

    def __iter__(self):
        """ Iterate the children of the node. """
        for childIndex in self._children:
            yield Node(childIndex, self._graph, self.index)

    @property
    def value(self):
        return self._graph.nodes[self.index]
