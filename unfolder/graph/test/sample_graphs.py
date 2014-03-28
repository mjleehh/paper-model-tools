from unfolder.graph.graph_builder import GraphBuilder


def createSimpleGraph():
    """
       A --- B
       :   / :
       : /   :
       D --- C
    """
    graphBuilder = GraphBuilder()
    graphBuilder.addNode('A', ['B', 'D'])
    graphBuilder.addNode('D', ['A', 'B', 'C'])
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
