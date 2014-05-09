class ModelImpl:
    def __init__(self, patches, flaps, connections, edges, vertices):
        self.patches = patches
        self.flaps = flaps
        self.connections = connections
        self.edges = edges
        self.vertices = vertices


class PatchImpl:
    def __init__(self, name, parentConnection, childConnections, borderEdges):
        self.name = name
        self.parentConnection = parentConnection
        self.childConnections = childConnections
        self.borderEdges = borderEdges

    def __repr__(self):
        res = '('
        res += 'p = ' + repr(self.parentConnection)
        res += ', c = ' + repr(self.childConnections)
        res += ')'
        return res


class EdgeImpl:
    def __init__(self, fstVertexIndex, sndVertexIndex):
        self.vertices = (fstVertexIndex, sndVertexIndex) if fstVertexIndex <= sndVertexIndex else (sndVertexIndex, fstVertexIndex)

    def __hash__(self):
        return hash(self.vertices)

    def __eq__(self, other):
        return self.vertices == other.vertices

    def __repr__(self):
        return repr(self.vertices)
