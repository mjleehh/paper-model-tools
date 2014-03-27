from unfolder.mesh.obj_mesh import ObjMesh, ObjFace, ObjEdge


class ObjImporter:
    """ Importer for Wavefront Obj files.
    """

    def __init__(self):
        self._faces = []
        self._edges = []
        self._edgeMapping = {}
        self._vertices = []
        self._textureCoords = []
        self._handlers = {'v': self.v, 'f': self.f}

    def handle(self, verb, nouns):
        if verb in self._handlers:
            self._handlers[verb](*nouns)

    def read(self,  file):
        with open(file) as f:
            for line in f:
                self.handleLine(line)
        return ObjMesh(self._faces, self._edges, self._vertices, self._textureCoords)

    def handleLine(self, line):
        words = line.split()
        if words:
            verb = words[0]
            self.handle(verb, words[1:])

    # handlers

    def v(self, x, y, z):
        self._vertices.append((float(x), float(y), float(z)))

    def f(self, *coords):
        textureCoords = self.getTextureCoords(coords)
        edges = self.getEdges(coords)
        self._faces.append(ObjFace(edges, textureCoords))

    def getTextureCoords(self, coords):
        parts = coords[0].split('/')
        if len(parts) > 1 and parts[1]:
            return [self.getTextureCoord(coord) for coord in coords]
        return None

    def getTextureCoord(self, tuple):
        textureCoord = int(tuple.split('/')[1])
        return textureCoord if textureCoord > 0 else textureCoord + len(self._textureCoords)

    def getVertex(self, tuple):
        vertexCoord = int(tuple.split('/')[0])
        return vertexCoord if vertexCoord > 0 else vertexCoord + len(self._vertices)

    def getEdges(self, coords):
        vertices = [self.getVertex(vertex) for vertex in coords]
        prevVertex = vertices[0]
        vertices = vertices[1:] + [prevVertex]
        edges = []

        for vertex in vertices:
            edgeIndex = self.addEdge(prevVertex, vertex)
            self._edges[edgeIndex].faces.append(len(self._faces))
            edges.append(edgeIndex)
            prevVertex = vertex
        return edges

    def addEdge(self, fst, snd):
        edge = ObjEdge(fst, snd)
        key = hash(edge)
        if key in self._edgeMapping:
            return self._edgeMapping[key]
        else:
            index = len(self._edges)
            self._edges.append(ObjEdge(fst, snd))
            self._edgeMapping[key] = index
            return index
