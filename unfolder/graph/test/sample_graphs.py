from unfolder.graph.graph import Graph
from unfolder.graph.graph_builder import GraphBuilder, buildGraph


def createSimpleGraph():
    """
       A --- B
       :   / :
       : /   :
       D --- C
    """
    return Graph(
        buildGraph()\
        .addNode('A', ['B', 'D'])\
        .addNode('D', ['A', 'B', 'C'])\
        .addNode('B', ['A', 'C', 'D'])\
        .addNode('C', ['B', 'D'])\
        .toGraph())


def createEmptyGraph():
    return Graph(
        buildGraph().toGraph())


def createSingularGraph():
    return Graph(
        buildGraph()\
        .addNode('A', [])\
        .toGraph())


def createPrimitiveGraph():
    """
       A - B
    """
    return Graph(
        buildGraph()\
        .addNode('A', ['B'])\
        .toGraph())


def createGraphWithTreeSpanningTrees():
    """
       A --- B
           / :
         /   :
       D --- C
    """
    return Graph(
        buildGraph()
        .addNode('A', ['B'])
        .addNode('B', ['A', 'C', 'D'])
        .addNode('C', ['B', 'D'])
        .toGraph())

def createSimpleTree():
    """
           A
          / \
         B   C
        /   / \
       D   E   F
    """
    return Graph(
        buildGraph()
        .addNode('A', ['B', 'C'])
        .addNode('B', ['D'])
        .addNode('C', ['E', 'F'])
        .toGraph())

def createGraphWithIsolatedNode():
    """
           A       F
          / \
         B   C
        /   /
       D   E
    """
    return Graph(
        buildGraph()
        .addNode('A', ['B', 'C'])
        .addNode('B', ['D'])
        .addNode('C', ['E'])
        .addNode('F', [])
        .toGraph())

def createDiamondGraph():
    """
       A --- B
         \ / :
         / \ :
       D --- C
    """
    return Graph(
        buildGraph()\
        .addNode('A', ['B', 'C', 'D'])\
        .addNode('B', ['A', 'C', 'D'])\
        .addNode('C', ['A', 'B', 'D'])\
        .addNode('D', ['A', 'B', 'C'])\
        .toGraph())
