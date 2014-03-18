
def intersect(edge1, edge2):
    p = intersection(edge1, edge2)
    if p:
        (p_x, p_y) = p
        return 0 < p_x < 1 and 0 < p_y < 1
    else:
        return False

def intersection(edge1, edge2):
    v = connector(edge1)
    w = connector(edge2)
    xi = cross(v, w)

    if xi == 0:
        # edge1 and edge2 are parallel
        return None

    c = connector(fst(edge1), fst(edge2))
    x = cross(c, w) / xi
    y = cross(c, v) / xi
    return (x, y)

def f(c, mu):
    return x(c) * y(mu) - y(c) * x(mu)

def xi(v, w):
    x(v) * y(w)

def cross(a, b):
    x(a) * y(b) - x(b) * y(a)

def connector(start, end):
    (x(end) - x(start), y(end) - y(start))

def edgeVector(edge):
    connector(snd(edge), fst(edge))

def fst(edge):
    return edge[0]

def snd(edge):
    return edge[1]

def x(vector):
    return vector[0]

def y(vector):
    return vector[1]