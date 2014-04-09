class Model:
    def __init__(self, patches, edges, vertices):
        self.patches = patches
        self.edges = edges
        self.vertices = vertices


class ModelPatch:
    def __init__(self, parentConnectionSet, connectionSets):
        self.parentConnectionSet = parentConnectionSet
        self.connectionSets = connectionSets

    def __repr__(self):
        res = '('
        res += 'p = ' + repr(self.parentConnectionSet)
        res += ', c = ' + repr(self.connectionSets)
        res += ')'
        return res


class PatchConnectionSet:
    def __init__(self, patch, edges, areGlued):
        self.patch = patch
        self.edges = edges
        self.areGlued = areGlued

    def __repr__(self):
        res = '('
        res += 'P = '+ self.patch
        res += ', E = ' + repr(self.edges)
        res += ', g = ' + repr(self.areGlued)
        res += ')'
        return res

class ModelEdge:
    def __init__(self, fst, snd):
        self.vertices = (fst, snd) if fst < snd else (snd, fst)

    def __hash__(self):
        return hash(self.vertices)

    def __eq__(self, other):
        return self.vertices == other.vertices

    def __repr__(self):
        return repr(self.vertices)
