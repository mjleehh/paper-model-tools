class ObjectFileReader:

    def __init__(self):
        self.vertices = []
        self.normals = []
        self.faces = []
        self._handlers = self._createHandlers()

    def _createHandlers(self):

        def v(x, y, z):
            self.vertices.append((float(x), float(y), float(z)))

        def vn(x, y, z):
            self.normals.append((float(x), float(y), float(z)))

        def determineFaceMode(coords):
            parts = coords[0].split('/')
            textureCoords = [] if len(parts) > 1 and parts[1] else None
            normals = [] if len(parts) > 2 else None
            return textureCoords, normals

        def f(*coords):
            vertices = []
            textureCoords, normals = determineFaceMode(coords)

            for coord in coords:
                splitCoords = coord.split('/')
                print(splitCoords)
                vertices.append(int(splitCoords[0]))
                if textureCoords is not None:
                    textureCoords.append(int(splitCoords[1]))
                if normals is not None:
                    normals.append(int(splitCoords[2]))

            self.faces.append((vertices, textureCoords, normals))

        return {'v': v, 'vn': vn, 'f': f}

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
