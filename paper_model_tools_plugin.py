import maya.OpenMayaMPx as omp
import sys

from unfolder.automatic_unfold.create_paper_model_command import CreatePaperModelCommand
from unfolder.automatic_unfold.create_paper_model_command2 import CreatePaperModelCommand2
from unfolder.select_facetree.create_paper_model_tool import CreatePaperModelTool


def createToolCommand():
    return omp.asMPxPtr(CreatePaperModelTool())


def createCommand():
    return omp.asMPxPtr(CreatePaperModelCommand())


def createCommand2():
    print('blub')
    return omp.asMPxPtr(CreatePaperModelCommand2())

kToolCommandName = "createPaperModelTool"
kCommandName = "createPaperModel"
kCommandName2 = "createPaperModel2"

# Initialize the script plug-in
def initializePlugin(mobject):
    print('Loading facetree selection plugin.')

    mplugin = omp.MFnPlugin(mobject, 'Michael Jonathan Lee', '0.1.0-SNAPSHOT')
    mplugin.setName('Paper Model Tools')

    try:
        mplugin.registerContextCommand(kToolCommandName, createToolCommand)
        mplugin.registerCommand(kCommandName, createCommand)
        mplugin.registerCommand(kCommandName2, createCommand2)
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
        mplugin.deregisterCommand(kCommandName2)
    except:
        sys.stderr.write('Failed to unregister commands')
