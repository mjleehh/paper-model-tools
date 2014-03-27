class ObjMesh():
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.faces = []

class ObjFace():
    def __init__(self, edges, textureCoords):
        self.edges = edges
        self.textureCoords = textureCoords

class ObjectFileReader:

    def __init__(self):
        self._mesh = ObjMesh()
        self._edgeMapping = {}
        self._handlers = self._createHandlers()

    def _createHandlers(self):

        return {'v': v, 'f': f}

    def handle(self, verb, nouns):
        if verb in self._handlers:
            self._handlers[verb](*nouns)

    def read(self,  file):
        with open(file) as f:
            for line in f:
                self.handleLine(line)

    def handleLine(self, line):
        words = line.split()
        if words:
            verb = words[0]
            self.handle(verb, words[1:])


    # handlers

    def v(self, x, y, z):
        self._mesh.vertices.append((float(x), float(y), float(z)))

    def f(self, *coords):
        edges = []
        textureCoords, normals = self._determineFaceMode(coords)

        prevVertex = None
        for coord in coords:
            splitCoords = coord.split('/')

            if textureCoords is not None:
                textureCoords.append(int(splitCoords[1]))

            vertex = (int(splitCoords[0]))

            # make relative vertex positions absolute
            if vertex < 0:
                vertex += len(self._mesh.vertices)

            if prevVertex:
                edges.append(self.addEdge(prevVertex, vertex))

            prevVertex = vertex

        self._mesh.faces.append(ObjFace(edges, textureCoords))

    def addEdge(self, fst, snd):
        key = frozenset((fst, snd))
        if key in self._edgeMapping:
            return self._edgeMapping[key]
        else:
            index = len(self._mesh.edges)
            self._mesh.edges.append((fst, snd))
            self._edgeMapping[key] = index
            return index

    @staticmethod
    def _determineFaceMode(coords):
            parts = coords[0].split('/')
            textureCoords = [] if len(parts) > 1 and parts[1] else None
            normals = [] if len(parts) > 2 else None
            return textureCoords, normals
