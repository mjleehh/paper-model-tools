from unfolder.automatic_unfold.mesh_to_graph import meshToGraph
from unfolder.tree.tree_impl import graphToTree
from unfolder.graph.graph_builder import GraphBuilder
from unfolder.graph.spanning_trees import SpanningTrees
from unfolder.mesh.obj_importer import ObjImporter
from unfolder.mesh.obj_mesh import MeshFaces
from unfolder.patch.treeToPatch import treeToPatch


def printTree(tree, depth=0):
    res = ' ' * depth
    res += str(tree.value)
    print(res)
    for child in tree:
        printTree(child, depth + 1)

mesh = ObjImporter().read('mesh/test/resources/box.obj')
faces = MeshFaces(mesh)
graph = meshToGraph(faces, GraphBuilder())
connectedComponents = graph.getConnectedComponents()

for connectedComponent in connectedComponents:
    for index, spanningTree in enumerate(SpanningTrees(connectedComponent)):
        print('spanningTree no %i' % index)
        tree = graphToTree(spanningTree)
        treeToPatch(tree, faces)
