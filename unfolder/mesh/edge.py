from unfolder.mesh.mesh_impl import MeshImpl


class Edge:
    def __init__(self, index, meshImpl: MeshImpl):
        self.meshImpl = meshImpl
        self.index = index

    def __getitem__(self, item):
        return self.meshImpl.vertices[self._value.vertices[item]]

    def __eq__(self, other):
        return self.index == other.index

    def __hash__(self):
        return hash(self.index)

    # private

    @property
    def _value(self):
        return self.meshImpl.edges[self.index]


# private


class EdgeIter:
    def __init__(self, meshImpl: MeshImpl):
        self.meshImpl = meshImpl

    def __iter__(self):
        for edgeIndex, val in enumerate(self.meshImpl.edges):
            yield self._item(edgeIndex)

    def __len__(self):
        return len(self.meshImpl.edges)

    def __getitem__(self, edgeIndex):
        return self._item(edgeIndex)

    # private

    def _item(self, edgeIndex):
        return Edge(edgeIndex, self.meshImpl)


class EdgeSubsetIter:
    def __init__(self, indices, meshImpl: MeshImpl):
        self.indices = indices
        self.meshImpl = meshImpl

    def __iter__(self):
        for edgeIndex in self.indices:
            yield self._item(edgeIndex)

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, item):
        return self._item(self.indices[item])

    # private

    def _item(self, edgeIndex):
        return Edge(edgeIndex, self.meshImpl)