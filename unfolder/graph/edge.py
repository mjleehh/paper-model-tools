from unfolder.graph.graph_impl import GraphImpl
from unfolder.graph.node import Node


class Edge:
    def __init__(self, index, graphImpl: GraphImpl):
        self.index = index
        self.graphImpl = graphImpl

    @property
    def nodes(self):
        return [Node(nodeIndex, self.graphImpl) for nodeIndex in self.impl.nodes]

    @property
    def impl(self):
        return self.graphImpl.edges[self.index]


# private


class EdgeIter:
    def __init__(self, graphImpl: GraphImpl):
        self.graphImpl = graphImpl

    def __iter__(self):
        for edgeIndex, val in enumerate(self.graphImpl.edges):
            yield self._item(edgeIndex)

    def __len__(self):
        return len(self.graphImpl.edges)

    def __getitem__(self, item):
        return self._item(item)

    # private

    def _item(self, edgeIndex):
        return Edge(edgeIndex, self.graphImpl)
