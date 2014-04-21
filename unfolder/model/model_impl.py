class ModelImpl:
    def __init__(self, patches, shadowPatches, connections, edges, vertices):
        self.patches = patches
        self.shadowPatches = shadowPatches
        self.connections = connections
        self.edges = edges
        self.vertices = vertices


class PatchImpl:
    def __init__(self, name, parentConnection, connections, borderEdges):
        self.name = name
        self.parentConnection = parentConnection
        self.connections = connections
        self.borderEdges = borderEdges

    def __repr__(self):
        res = '('
        res += 'p = ' + repr(self.parentConnection)
        res += ', c = ' + repr(self.connections)
        res += ')'
        return res


class ConnectionImpl:
    def __init__(self, edges):
        # index of first patch < index of second patch
        self.edges = edges

    def __repr__(self):
        res = '('
        res += 'E = ' + repr(self.edges)
        res += ')'
        return res


class ShadowPatchImpl:
    def __init__(self, patch, parentConnection, vertices):
        self.patch = patch
        self.parentConnection = parentConnection
        self.vertices = vertices

class EdgeImpl:
    def __init__(self, fstVertexIndex, sndVertexIndex):
        self.vertices = (fstVertexIndex, sndVertexIndex) if fstVertexIndex <= sndVertexIndex else (sndVertexIndex, fstVertexIndex)

    def __hash__(self):
        return hash(self.vertices)

    def __eq__(self, other):
        return self.vertices == other.vertices

    def __repr__(self):
        return repr(self.vertices)
