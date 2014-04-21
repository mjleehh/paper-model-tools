from unfolder.graph.graph import Graph
from unfolder.graph.graph_impl import GraphImpl


class SpanningTreeIter:

    def __init__(self, graph: Graph):
        self.graph = graph.copy().impl
        self.graph.edges.sort(key=lambda edge: edge.nodes[0])

        # initial tree
        self.T_0 = graph.getSpanningTree().impl

        self._entrablesForSpanningTreeEdge = Entrables(self.T_0, self.graph).getEntrablesForSpanningTreeEdge

    def __iter__(self):
        V = len(self.T_0.edges)
        yield self.T_0
        for T in self._derivedSpanningTrees(self.T_0, V - 1):
            yield T

    def _derivedSpanningTrees(self, T_p, k):
        if k >= 0:
            e_k = self.T_0.edges[k]
            for g in self._entrablesForSpanningTreeEdge(T_p, e_k):
                T_c = self._replaceEdge(T_p, e_k, g)
                if T_c and Graph(T_c).isTree():
                    yield T_c
                    for T in self._derivedSpanningTrees(T_c, k - 1):
                        yield T
            for T in self._derivedSpanningTrees(T_p, k - 1):
                yield T

    def _replaceEdge(self, T_p, e_k, g):
        T_c = Graph(T_p).copy().impl
        index = T_c.edges.index(e_k)
        T_c.edges[index] = g
        return T_c


# private


class FundamentalCuts:

    def __init__(self, graph: Graph):
        self._allEdges = set(graph.edges)

    def getCutFromSpanningTreeEdge(self, spanningTree, cutEdge):
        if not cutEdge in spanningTree.edges:
            raise ValueError('edge ' + str(cutEdge) + ' is not in spanning tree ' + str(spanningTree))
        newTree = Graph(spanningTree).copy().impl
        candidateEdges = self._allEdges - set(newTree.edges)

        res = []
        cutEdgeIndex = newTree.edges.index(cutEdge)
        for edge in candidateEdges:
            newTree.edges[cutEdgeIndex] = edge
            if Graph(newTree).isTree():
                res.append(edge)
        return set(res)


class Entrables:

    def __init__(self, initialTree, graph: Graph):
        self._initialTree = initialTree
        self._initialTreeCutCache = {}
        self._getFundamentalCut = FundamentalCuts(graph).getCutFromSpanningTreeEdge

    def getEntrablesForSpanningTreeEdge(self, tree, edge):
        initialTreeCut = self._getInitialTreeCut(edge)
        treeCut = self._getFundamentalCut(tree, edge)
        for elem in initialTreeCut & treeCut:
            yield elem

    # private

    def _getInitialTreeCut(self, edge):
        if not edge in self._initialTreeCutCache:
            cut = self._getFundamentalCut(self._initialTree, edge)
            self._initialTreeCutCache[edge] = cut
            return cut
        else:
            return self._initialTreeCutCache[edge]

