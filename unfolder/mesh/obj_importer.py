from unfolder.mesh.mesh_impl import MeshImpl, EdgeImpl, FaceImpl


class ObjImporter:
    """ Importer for Wavefront Obj files.
    """

    def __init__(self):
        self._faces = []
        self._edges = []
        self._edgeMapping = {}
        self._vertices = []
        self._textureCoords = []
        self._handlers = {'v': self.v, 'vt' : self.vt, 'f': self.f}

    def read(self,  file):
        with open(file) as f:
            for line in f:
                self._handleLine(line)
        return MeshImpl(self._faces, self._edges, self._vertices, self._textureCoords)

    # handlers

    def v(self, x, y, z):
        self._vertices.append((float(x), float(y), float(z)))

    def f(self, *coords):
        textureCoords = self._getTextureCoords(coords)
        edges = self._getEdges(coords)
        self._faces.append(FaceImpl(edges, textureCoords))

    def vt(self, x, y):
        self._textureCoords.append((float(x), float(y)))

    # private

    def _handle(self, verb, nouns):
        if verb in self._handlers:
            self._handlers[verb](*nouns)

    def _handleLine(self, line):
        words = line.split()
        if words:
            verb = words[0]
            self._handle(verb, words[1:])

    def _getTextureCoords(self, coords):
        parts = coords[0].split('/')
        if len(parts) > 1 and parts[1]:
            return [self._getTextureCoord(coord) for coord in coords]
        return None

    def _getTextureCoord(self, tuple):
        textureCoord = int(tuple.split('/')[1]) - 1
        return textureCoord if textureCoord >= 0 else textureCoord + len(self._textureCoords)

    def _getVertex(self, tuple):
        vertexCoord = int(tuple.split('/')[0]) - 1
        return vertexCoord if vertexCoord >= 0 else vertexCoord + len(self._vertices)

    def _getEdges(self, coords):
        vertices = [self._getVertex(vertex) for vertex in coords]
        prevVertex = vertices[0]
        vertices = vertices[1:] + [prevVertex]
        edges = []

        for vertex in vertices:
            edgeIndex = self._addEdge(prevVertex, vertex)
            edges.append(edgeIndex)
            prevVertex = vertex
        return edges

    def _addEdge(self, fst, snd):
        edge = EdgeImpl(fst, snd)
        key = hash(edge)
        if key in self._edgeMapping:
            return self._edgeMapping[key]
        else:
            index = len(self._edges)
            self._edges.append(EdgeImpl(fst, snd))
            self._edgeMapping[key] = index
            return index
