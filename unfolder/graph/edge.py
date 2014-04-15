class Edge:
    def __init__(self, fstIndex, sndIndex):
        if fstIndex == sndIndex:
            raise ValueError('Loop detected ' + str(fstIndex))
        self.nodeIndices = (fstIndex, sndIndex) if fstIndex < sndIndex else (sndIndex, fstIndex)

    def hasNode(self, nodeIndex):
        return self.fst() == nodeIndex or self.snd() == nodeIndex

    def getOther(self, nodeIndex):
        if self.fst() == nodeIndex:
            return self.snd()
        elif self.snd() == nodeIndex:
            return self.fst()
        else:
            return None

    def __eq__(self, other):
        return self.nodeIndices == other.nodeIndices

    def __hash__(self):
        return hash(self.nodeIndices)

    def __repr__(self):
        return str(self.nodeIndices)

    def fst(self):
        return self.nodeIndices[0]

    def snd(self):
        return self.nodeIndices[1]
