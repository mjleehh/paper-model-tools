class GraphImpl:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def __repr__(self):
        retval = 'G = (\n  V = {'
        delim = ''
        for node in self.nodes:
            retval += delim + repr(node)
            delim = ', '
        retval += '},\n  E = {'
        delim = ''
        for edge in self.edges:
            retval += delim + repr(edge)
            delim = ', '
        retval += "}\n)"
        return retval


class EdgeImpl:
    def __init__(self, fstIndex, sndIndex):
        if fstIndex == sndIndex:
            raise ValueError('Loop detected ' + str(fstIndex))
        self.nodes = (fstIndex, sndIndex) if fstIndex < sndIndex else (sndIndex, fstIndex)

    def __eq__(self, other):
        return self.nodes == other.nodes

    def __hash__(self):
        return hash(self.nodes)