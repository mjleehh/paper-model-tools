class Model:
    def __init__(self, patches, vertices):
        self.patches = patches
        self.vertices = vertices


class ModelPatch:
    def __init__(self, parentEdges, sharedEdges, glueEdges, borderEdges):
        self.parentEdges = parentEdges
        self.sharedEdges = sharedEdges
        self.glueEdges = glueEdges
        self.borderEdges = borderEdges


class PatchEdge:
    def __init__(self, nextPatchIndex, fst, snd, terminal = False):
        self.terminal = terminal
        self.nextPatchIndex = nextPatchIndex
        self.vertices = (fst, snd) if fst < snd else (snd, fst)
