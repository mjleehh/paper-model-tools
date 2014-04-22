from unfolder.graph.graph_impl import GraphImpl, EdgeImpl
from unfolder.graph.node import Node
from unfolder.tree.knot import Knot


def createSimpleTree():
    """
                             'f'[5]
                          /          \
                         / 3         \ 1
                        /            \
                  *'d'[3]             'a '[0]
                 /      \           /      \
                / 2     \ 4        / 0     \ 6
               /        \         /        \
            'e'[4]    'c'[2]    'h'[7]     'g'[6]
            /
           / 5
          /
        'b'[1]

    """
    nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    edges = [(0, 7), (5, 0), (3, 4), (5, 3), (3, 2), (4, 1), (0, 6)]
    graphEdges = [EdgeImpl(fst, snd) for fst, snd in edges]
    return Knot(Node(5, GraphImpl(nodes, graphEdges)))


def createPyramidTree():
    nodes = ['a', 'b', 'c', 'd', 'e']
    edges = [(4, 0), (0, 3), (3, 2), (2, 1)]
    graphEdges = [EdgeImpl(fst, snd) for fst, snd in edges]
    return Knot(Node(0, GraphImpl(nodes, graphEdges)))