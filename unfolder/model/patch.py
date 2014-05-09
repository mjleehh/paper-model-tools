from unfolder.model.model_impl import ModelImpl, PatchImpl
from unfolder.util.appenders import StackBuckets


def getOther(elem, bituple):
    (fst, snd) = bituple
    if elem == fst:
        return snd
    elif elem == snd:
        return fst
    else:
        raise Exception('Error element ' + repr(elem) + ' is not in ' + repr(bituple))

class Patch:
    def __init__(self, index, modelImpl: ModelImpl):
        self.index = index
        self.modelImpl = modelImpl

    @property
    def edges(self):
        edgesByVertex = self._getEdgesByVertex()
        edgeIndex = initialEdgeIndex = self._getInitialEdge()
        vertexIndex = self.modelImpl.edges[edgeIndex].vertices[0]
        edges = []
        while True:
            edges.append(edgeIndex)
            edgeIndex = getOther(edgeIndex, edgesByVertex[vertexIndex])
            vertexIndex = getOther(vertexIndex, self.modelImpl.edges[edgeIndex].vertices)
            if edgeIndex == initialEdgeIndex:
                break
        return edges

    @property
    def vertices(self):
        edgesByVertex = self._getEdgesByVertex()
        edgeIndex = initialEdgeIndex = self._getInitialEdge()
        vertexIndex = self.modelImpl.edges[edgeIndex].vertices[0]
        vertices = []
        while True:
            vertices.append(vertexIndex)
            edgeIndex = getOther(edgeIndex, edgesByVertex[vertexIndex])
            vertexIndex = getOther(vertexIndex, self.modelImpl.edges[edgeIndex].vertices)
            if edgeIndex == initialEdgeIndex:
                break
        return vertices

    def _getInitialEdge(self):
        initialConnectionIndex = self.impl.parentConnection if self.impl.parentConnection is not None \
            else self.impl.childConnections[0]
        return self.modelImpl.connections[initialConnectionIndex][0]

    def _getEdgesByVertex(self):
        def addEdge(connectionIndex):
            for edgeIndex in self.modelImpl.connections[connectionIndex]:
                (fstVertex, sndVertex) = self.modelImpl.edges[edgeIndex].vertices
                buckets.push(fstVertex, edgeIndex)
                buckets.push(sndVertex, edgeIndex)

        buckets = StackBuckets()
        if self.impl.parentConnection is not None:
            addEdge(self.impl.parentConnection)
        for connection in self.impl.childConnections:
            addEdge(connection)
        return buckets.store

    @property
    def name(self):
        return self.impl.name

    @property
    def impl(self):
        return self.modelImpl.patches[self.index]


# private


class PatchIter:
    def __init__(self, modelImpl: ModelImpl):
        self.modelImpl = modelImpl

    def __iter__(self):
        for patchIndex, val in enumerate(self.modelImpl.patches):
            yield self._item(patchIndex)

    def __len__(self):
        return len(self.modelImpl.patches)

    def __getitem__(self, patchIndex):
        return self._item(patchIndex)

    # private

    def _item(self, patchIndex):
        return Patch(patchIndex, self.modelImpl)
