import maya.OpenMayaMPx as omp

from .select_facetree_context import SelectFacetreeContext
from .state_factory import StateFactory


class CreatePaperModelTool(omp.MPxContextCommand):
    def __init__(self):
        omp.MPxContextCommand.__init__(self)
        print('constructed')

    def makeObj(self):
        print('created')
        return omp.asMPxPtr(SelectFacetreeContext(StateFactory()))