from unfolder.analyze_patch.model_score import calculateModelScore
from unfolder.automatic_unfold.mesh_to_graph import meshToGraph
from unfolder.tree.tree_impl import graphToTree
from unfolder.graph.graph_builder import GraphBuilder
from unfolder.graph.spanning_trees import SpanningTrees
from unfolder.mesh.obj_importer import ObjImporter
from unfolder.mesh.obj_mesh import MeshFaces
from unfolder.model.tree_to_model import treeToModel


def printTree(tree, depth=0):
    res = ' ' * depth
    res += str(tree.value)
    print(res)
    for child in tree:
        printTree(child, depth + 1)

# load a sample file
mesh = ObjImporter().read('mesh/test/resources/box.obj')
# create an accessor to the mesh faces
faces = MeshFaces(mesh)
# create a graph from the mesh's face structure information
# each graph node holds the index of the corresponding face
graph = meshToGraph(faces, GraphBuilder())

# create a model from every connected set of faces
for connectedComponent in graph.getConnectedComponents():
    # iterate all spanning trees of the graph
    # each spanning tree corresponds to one of the possible models
    for index, spanningTree in enumerate(SpanningTrees(connectedComponent)):
        print('spanningTree no %i' % index)
        tree = graphToTree(spanningTree)
        model = treeToModel(tree, faces)
        score = calculateModelScore(model)