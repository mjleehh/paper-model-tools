import maya.OpenMayaMPx as omp
import sys

from unfolder.automatic_unfold.create_paper_model_command import CreatePaperModelCommand
from unfolder.select_facetree.create_paper_model_tool import CreatePaperModelTool


def createToolCommand():
    return omp.asMPxPtr(CreatePaperModelTool())


def createCommand():
    return omp.asMPxPtr(CreatePaperModelCommand())


kToolCommandName = "createPaperModelTool"
kCommandName = "createPaperModel"


# Initialize the script plug-in
def initializePlugin(mobject):
    print('Loading facetree selection plugin.')

    mplugin = omp.MFnPlugin(mobject, 'Michael Jonathan Lee', '0.1.0-SNAPSHOT')
    mplugin.setName('Paper Model Tools')

    try:
        mplugin.registerContextCommand(kToolCommandName, createToolCommand)
        mplugin.registerCommand(kCommandName, createCommand)
    except:
        sys.stderr.write('Failed to register commands')
        raise


# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    print('unload')

    mplugin = omp.MFnPlugin(mobject)
    try:
        mplugin.deregisterContextCommand(kToolCommandName)
        mplugin.deregisterCommand(kCommandName)
    except:
        sys.stderr.write('Failed to unregister commands')
