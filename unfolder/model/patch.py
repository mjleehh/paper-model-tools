from unfolder.model.model_impl import ModelImpl, PatchImpl
from unfolder.util.appenders import StackBuckets


class Patch:
    def __init__(self, index, modelImpl: ModelImpl):
        self.index = index
        self.modelImpl = modelImpl

    @property
    def edges(self):
        edgesByVertex = self._getEdgesByVertex()
        #print(next(iter(edgesByVertex.items())))
        return edgesByVertex

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
