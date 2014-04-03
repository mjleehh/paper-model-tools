class Patch:
    def __init__(self, faces, vertices):
        self.faces = faces
        self.vertices = vertices


class PatchFace:
    def __init__(self, parentEdge, edges):
        self.parentEdge = parentEdge
        self.edges = edges


class PatchEdge:
    def __init__(self, face, fst, snd, terminal = False):
        self.terminal = terminal
        self.faces = face
        self.vertices = (fst, snd) if fst < snd else (snd, fst)
