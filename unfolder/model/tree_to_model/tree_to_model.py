from unfolder.mesh.face import FaceIter
from unfolder.model.tree_to_model.edge_proxy import PatchEdgeProxy
from unfolder.model.model import Model
from unfolder.model.model_builder import ModelBuilder
from unfolder.model.tree_to_model.patch_base import PatchBase
from unfolder.model.tree_to_model.patch_builder import PatchBuilder

from unfolder.tree.knot import Knot


def treeToModel(tree: Knot, meshFaces):
    return TreeToModelConverter(meshFaces, None).convert(tree)


# private


class TreeToModelConverter:
    def __init__(self, meshFaces: FaceIter, patchBuilder):
        self._meshFaces = meshFaces
        # the model normal
        self.modelBuilder = ModelBuilder((0., 0., 1.))
        self._patchMapping = {}

    def convert(self, tree: Knot):
        origin = (0., 0., 0.)
        fst = (1., 0., 0.)
        baseEdge = PatchEdgeProxy(origin, fst)
        inBaseEdge = self._meshFaces[tree.value].edges[0]
        self._flattenSubtree(tree, PatchBase(None, None, inBaseEdge, baseEdge))
        return Model(self.modelBuilder.build())

    def _flattenSubtree(self, subtree, patchBase):
        thisFace = self._meshFaces[subtree.value]
        patchBuilder = PatchBuilder(thisFace, patchBase, self.modelBuilder)

        children = set()

        for child in subtree:
            childFace = self._meshFaces[child.value]
            children.add(childFace)
            childPatchBase = patchBuilder.addConnection(childFace)
            self._flattenSubtree(child, childPatchBase)

        disconnectedFaces = set(thisFace.getConnectedFaces()) - children
        if patchBase.parentFace is not None:
            disconnectedFaces.remove(patchBase.parentFace)

        for disconnectedFace in disconnectedFaces:
            childPatchBase = patchBuilder.addConnection(disconnectedFace)

        self._patchMapping[thisFace] = self.modelBuilder.addPatch(patchBuilder.build())

