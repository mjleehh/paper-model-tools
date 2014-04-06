class ObjMesh():
    def __init__(self, faces, edges, vertices, textureCoords):
        self.faces = faces
        self.edges = edges
        self.vertices = vertices
        self.textureCoords = textureCoords


class ObjFace():
    def __init__(self, edges, textureCoords):
        self.edges = edges
        self.textureCoords = textureCoords

    def __repr__(self):
        res = '(E = ['
        delim = ''
        for edge in self.edges:
            res += delim
            res += str(edge)
            delim = ', '
        res += '])'
        return res


class ObjEdge():
    def __init__(self, fst, snd):
        self.faces = []
        self.vertices = (fst, snd) if fst < snd else (snd, fst)

    def __hash__(self):
        return hash(self.vertices)

    def __eq__(self, other):
        return self.vertices == other.vertices

    def __repr__(self):
        return str(self.vertices)
