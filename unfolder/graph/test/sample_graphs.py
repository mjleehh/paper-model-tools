from unfolder.graph.graph_builder import GraphBuilder, buildGraph


def createSimpleGraph():
    """
       A --- B
       :   / :
       : /   :
       D --- C
    """
    return buildGraph()\
        .addNode('A', ['B', 'D'])\
        .addNode('D', ['A', 'B', 'C'])\
        .addNode('B', ['A', 'C', 'D'])\
        .addNode('C', ['B', 'D'])\
        .toGraph()


def createEmptyGraph():
    return buildGraph().toGraph()


def createSingularGraph():
    return buildGraph()\
        .addNode('A', [])\
        .toGraph()


def createPrimitiveGraph():
    """
       A - B
    """
    return buildGraph()\
        .addNode('A', ['B'])\
        .toGraph()


def createGraphWithTreeSpanningTrees():
    """
       A --- B
           / :
         /   :
       D --- C
    """
    graphBuilder = GraphBuilder()
    graphBuilder.addNode('A', ['B'])
    graphBuilder.addNode('B', ['A', 'C', 'D'])
    graphBuilder.addNode('C', ['B', 'D'])
    return graphBuilder.toGraph()

def createSimpleTree():
    """
           A
          / \
         B   C
        /   / \
       D   E   F
    """
    graphBuilder = GraphBuilder()
    graphBuilder.addNode('A', ['B', 'C'])
    graphBuilder.addNode('B', ['D'])
    graphBuilder.addNode('C', ['E', 'F'])
    return graphBuilder.toGraph()

def createGraphWithIsolatedNode():
    """
           A       F
          / \
         B   C
        /   /
       D   E
    """
    graphBuilder = GraphBuilder()
    graphBuilder.addNode('A', ['B', 'C'])
    graphBuilder.addNode('B', ['D'])
    graphBuilder.addNode('C', ['E'])
    graphBuilder.addNode('F', [])
    return graphBuilder.toGraph()

def createDiamondGraph():
    """
       A --- B
         \ / :
         / \ :
       D --- C
    """
    return buildGraph()\
        .addNode('A', ['B', 'C', 'D'])\
        .addNode('B', ['A', 'C', 'D'])\
        .addNode('C', ['A', 'B', 'D'])\
        .addNode('D', ['A', 'B', 'C'])\
        .toGraph()
