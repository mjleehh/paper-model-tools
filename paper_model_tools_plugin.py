import sys

import maya.OpenMayaMPx as omp
from unfolder.select_facetree.select_facetree_context import SelectFacetreeContext
from unfolder.select_facetree.state_factory import StateFactory


class FacetreeSelectionCommand(omp.MPxContextCommand):
    def __init__(self):
        omp.MPxContextCommand.__init__(self)
        print('constructed')

    def makeObj(self):
        print('created')
        return omp.asMPxPtr(SelectFacetreeContext(StateFactory()))

# Creator
def createCommand():
    return omp.asMPxPtr(FacetreeSelectionCommand())


kPluginCmdName = "selectFacetree"


# Initialize the script plug-in
def initializePlugin(mobject):
    print('Loading facetree selection plugin.')

    mplugin = omp.MFnPlugin(mobject, 'Michael Jonathan Lee', '0.1.0-SNAPSHOT')
    mplugin.setName('Paper Model Tools')

    try:
        mplugin.registerContextCommand(kPluginCmdName, createCommand)
    except:
        sys.stderr.write("Failed to register command: %s\n" % kPluginCmdName)
        raise


# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    print('unload')

    mplugin = omp.MFnPlugin(mobject)
    try:
        mplugin.deregisterContextCommand(kPluginCmdName)
    except:
        sys.stderr.write("Failed to unregister command: %s\n" % kPluginCmdName)
