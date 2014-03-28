
def spanningTrees(graph):
    n = graph.numNodes()
    T_0 = graph.getSpanningTree()
    for T in derivedSpanningTrees(T_0, n - 1, graph.getEdges()):
        yield T

def derivedSpanningTrees(T_p, k, edges):
    if k > 0:
        for T_c in edges:
            T_c = T_p.replaceEdge(edges[k], k)
            if T_c.isTree():
                yield T_c
            for T in derivedSpanningTrees(T_c, k - 1, edges):
                yield T
