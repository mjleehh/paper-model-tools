class BoundingRect:
    def __init__(self):
        self._left   = None
        self._top    = None
        self._right  = None
        self._bottom = None

    def add(self, vertex):
        if self._left:
            self._left   = min(x(vertex), self._left)
            self._top    = max(y(vertex), self._top)
            self._right  = max(x(vertex), self._right)
            self._bottom = min(y(vertex), self._bottom)
        else:
            self._left   = x(vertex)
            self._top    = y(vertex)
            self._right  = x(vertex)
            self._bottom = y(vertex)

    def contains(self, vertex):
        return self._left < x(vertex) < self._right and self._bottom < y(vertex) < self._top


class InnerVertexChecker:

    def __init__(self, edges):
        upwardEdges = [makeEdgeUpward(edge) for edge in edges]
        self._edges = sorted(upwardEdges, fstY)
        boundingRect = BoundingRect()
        for edge in edges:
            boundingRect.add(fst(edge))
            boundingRect.add(snd(edge))
        self._boundingRect = boundingRect

    def isInnerVertex(self, vertex):
        if not self._boundingRect.contains(vertex):
            return False
        scanlineY = y(vertex)
        intersectingEdges = getIntersectingEdges(self._edges)
        numIntersectionsLeftOfVertex = 0
        for edge in intersectingEdges:
            if xIntersection(scanlineY, edge) < x(vertex):
                numIntersectionsLeftOfVertex += 1


def xIntersection(p_y, edge):
    a_x = x(fst(edge))
    a_y = y(fst(edge))
    b_x = x(snd(edge))
    b_y = y(snd(edge))
    xi = b_y - a_y
    if xi == 0:
        return None
    return (p_y - a_y) * (b_x - a_x) / xi + a_x


def getIntersectingEdges(scanlineY, edges):
    retval = []
    for edge in edges:
        if not y(fst(edge)) < scanlineY:
            break
        if scanlineY < y(snd(edge)):
            retval.append(edge)
    return retval


def fstY(edge):
    return y(fst(edge))


def makeEdgeUpward(edge):
    if y(snd(edge)) < y(snd(edge)):
        return [snd(edge), fst(edge)]
    else:
        return edge


def fst(edge):
    return edge[0]


def snd(edge):
    return edge[1]


def x(vertex):
    return vertex[0]


def y(vertex):
    return vertex[1]