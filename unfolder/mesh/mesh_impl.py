class MeshImpl:
    def __init__(self, faces, edges, vertices, textureCoords):
        self.faces = faces
        self.edges = edges
        self.vertices = vertices
        self.textureCoords = textureCoords


class FaceImpl:
    def __init__(self, edges, textureCoords):
        self.edges = edges
        self.textureCoords = textureCoords

    def __repr__(self):
        res = '('
        res += 'E = ' + repr(self.edges)
        res += ')'
        return res


class EdgeImpl:
    def __init__(self, fst, snd):
        self.vertices = (fst, snd) if fst < snd else (snd, fst)

    def __hash__(self):
        return hash(self.vertices)

    def __eq__(self, other):
        return self.vertices == other.vertices

    def __repr__(self):
        return repr(self.vertices)
