from unfolder.graph.graph_impl import GraphImpl


class Node:
    def __init__(self, index, graphImpl: GraphImpl):
        self.index = index
        self.graphImpl = graphImpl

    @property
    def value(self):
        return self.graphImpl.nodes[self.index]

    @property
    def connectedNodes(self):
        def getOther(edge, nodeIndex):
            nodes = edge.nodes
            return nodes[not nodes.index(nodeIndex)]
        nodeIndices =  [getOther(edge, self.index) for edge in self.graphImpl.edges if self.index in edge.nodes]
        return NodeSubsetIter(nodeIndices, self.graphImpl)

    def __eq__(self, other):
        return self.index == other.index

    def __hash__(self):
        return hash(self.index)


# private


class NodeSubsetIter:
    def __init__(self, indices, graphImpl: GraphImpl):
        self.indices = indices
        self.graphImpl = graphImpl

    def __iter__(self):
        for nodeIndex in self.indices:
            yield self._item(nodeIndex)

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, item):
        return self._item(self.indices[item])

    # private

    def _item(self, nodeIndex):
        return Node(nodeIndex, self.graphImpl)
