import maya.OpenMaya as om
import maya.OpenMayaMPx as omp

from facetree import createFacetreeSelectionOrder
from patch import flattenTree
from patchbuilder import MeshPatchBuilder

import sys


class Selection:
    """ Save and restore the selection. """
    def __init__(self):
        """ Store the current selection. """
        selection = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection)
        self.selection = selection
        self.componentSelectionMask = om.MGlobal.componentSelectionMask()
        self.selectionMode = om.MGlobal.selectionMode()

    def makeCurrent(self):
        """ Replace the current selection with the stored one. """
        om.MGlobal.setSelectionMode(self.selectionMode)
        om.MGlobal.setComponentSelectionMask(self.componentSelectionMask)
        om.MGlobal.setActiveSelectionList(self.selection)


class DoNothing():
    """ Do nothing on input. When the context has been completed it remains in
        this state.
    """
    def __init__(self, context):
        self.context = context

    def selectionChanged(self):
        print('nothing callback')
        return self

    def delete(self):
        print('nothing delete')
        return self

    def complete(self):
        print('nothing complete')
        return self

    def abort(self):
        print('nothing abort')
        return self


class SelectObject(DoNothing):
    """ Select an object for the select faces in order tool. """

    def __init__(self, context):
        DoNothing.__init__(self, context)
        self._context = context
        context.listen()

    def selectionChanged(self):
        print('select callback')
        primarySelection = self._getPrimarySelection()
        if primarySelection:
            self._context.unlisten()
            return SelectFacesInOrder(self._context, primarySelection)
        else:
            self._context._setHelpString('Select an object')
            return self

    def delete(self):
        print('select delete')
        return self.abort()

    def complete(self):
        print('select complete')
        return self.abort()

    def abort(self):
        om.MGlobal.displayWarning('Nothing done.')
        self._context.unlisten()
        print('select abort')
        return DoNothing(self._context)

    def _getPrimarySelection(self):
        selection = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection)

        if not selection.isEmpty():
            dagPath = om.MDagPath()
            selection.getDagPath(0, dagPath)
            return dagPath
        else:
            return None


class SelectFacesInOrder(DoNothing):
    """ Select faces in order. """

    def __init__(self, context, dagPath):
        DoNothing.__init__(self, context)
        self._context = context
        self._dagPath = dagPath
        self._faces = []
        self._selectableFaces = None
        self._patchBuilder = MeshPatchBuilder()
        om.MGlobal.setSelectionMode(om.MGlobal.kSelectComponentMode)
        om.MGlobal.setComponentSelectionMask(om.MSelectionMask(om.MSelectionMask.kSelectMeshFaces))
        hiliteList = om.MSelectionList()
        hiliteList.add(dagPath)
        om.MGlobal.setActiveSelectionList(hiliteList)
        om.MGlobal.setHiliteList(hiliteList)
        context._setHelpString('Select faces in order')
        context.listen()

    def selectionChanged(self):
        self._context.unlisten()
        selection = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection)
        if not selection.length() is 0:
            print('order evaluate')
            dagPath = om.MDagPath()
            components = om.MObject()
            selection.getDagPath(0, dagPath, components)
            print(dagPath.fullPathName())
            faces = om.MIntArray()
            print(components.apiTypeStr())
            a = om.MFnSingleIndexedComponent(components)
            a.getElements(faces)

            newFaces = frozenset(faces) - frozenset(self._faces)
            if self._selectableFaces:
                newFaces = newFaces & self._selectableFaces
            self._faces.extend(newFaces)
            print('faces: ' + str(self._faces))
            print('new faces ' + str(newFaces))

            self.flatten()

            self._selectFaces()
            self._context.listen()
            return self
        print('selection was empty')
        return self.abort()

    def flatten(self):
        tree = createFacetreeSelectionOrder(self._dagPath, self._faces)
        self._patchBuilder.reset()
        flattenTree(self._dagPath, tree, self._patchBuilder)


    def delete(self):
        self._context.unlisten()
        self._faces.pop()
        self.flatten()
        self._selectFaces()
        self._context.listen()
        print('order delete')
        return self

    def complete(self):
        self.flatten()
        print('order complete')
        return self.abort()

    def abort(self):
        self._context.unlisten()
        print('order abort')
        return DoNothing(self._context)

    def _selectFaces(self):
        faceComponents = om.MFnSingleIndexedComponent()
        faceComponents.create(om.MFn.kMeshPolygonComponent)
        for face in self._faces:
            faceComponents.addElement(face)

        selection = om.MSelectionList()
        selection.add(self._dagPath, faceComponents.object())
        om.MGlobal.setActiveSelectionList(selection)
        self._updateSelectableFaces(faceComponents)

    def _updateSelectableFaces(self, faceComponents):
        if self._faces:
            allConnectedFaces = []
            faceIter = om.MItMeshPolygon(self._dagPath, faceComponents.object())
            while not faceIter.isDone():
                connectedFaces = om.MIntArray()
                faceIter.getConnectedFaces(connectedFaces)
                allConnectedFaces.extend(connectedFaces)
                faceIter.next()
                self._selectableFaces = frozenset(allConnectedFaces)


class FacetreeSelectionContext(omp.MPxSelectionContext):
    def __init__(self):
        omp.MPxSelectionContext.__init__(self)
        self._state = None
        self._callback = None
        self._selection = None

    def toolOnSetup(self, event):
        """ Called each time the context is activated. """
        self._selection = Selection()
        self._state = SelectObject(self)
        self._state.selectionChanged()

    def toolOffCleanup(self):
        """ Called each time the context is deactivated. """
        self.unlisten()
        if self._selection:
            self._selection.makeCurrent()
            self._selection = None
        self._state = None
        print('cleanup')
        self.unlisten()

    def completeAction(self):
        """ Complete the tool (enter has been pressed). """
        self._state.complete()

    def deleteAction(self):
        """ Go one step back (backspace has been pressed). """
        self._state.delete()

    def abortAction(self):
        """ Abort the tool (escape has been pressed). """
        self._state.abort()

    def selectionChanged(self):
        """ Called when the selection has changed. """
        self._state = self._state.selectionChanged()

    def listen(self):
        """ Enable callback for selection changes. """
        self._callback = om.MModelMessage.addCallback(om.MModelMessage.kActiveListModified, selectionChanged, self)

    def unlisten(self):
        """ Disable callback for selection changes. """
        if self._callback:
                om.MModelMessage.removeCallback(self._callback)
                self._callback = None


def selectionChanged(context):
    """ Callback for selection changes.

    Delegates handling to context instance. """
    context.selectionChanged()


class FacetreeSelectionCommand(omp.MPxContextCommand):
    def __init__(self):
        omp.MPxContextCommand.__init__(self)

    def makeObj(self):
        return omp.asMPxPtr(FacetreeSelectionContext())


# Creator
def createCommand():
    return omp.asMPxPtr(FacetreeSelectionCommand())


kPluginCmdName = "selectFacetree"


# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = omp.MFnPlugin(mobject)
    try:
        mplugin.registerContextCommand(kPluginCmdName, createCommand)
    except:
        sys.stderr.write("Failed to register command: %s\n" % kPluginCmdName)
        raise


# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = omp.MFnPlugin(mobject)
    try:
        mplugin.deregisterContextCommand(kPluginCmdName)
    except:
        sys.stderr.write("Failed to unregister command: %s\n" % kPluginCmdName)
