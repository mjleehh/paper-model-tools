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
    """ Final state of the face tree selection tool.

        Do nothing on input. When the context has been completed it remains in
        this state.
    """
    def __init__(self, context):
        self._context = context

    def init(self):
        self._context.listen()
        self._context.setHelpString('face tree selection tool done')
        return self

    def advance(self, nextState):
        print('advance')
        self._context.unlisten()
        return nextState.init()

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
    """ Select an object for the face tree selection tool. """

    def __init__(self, context):
        DoNothing.__init__(self, context)

    def init(self):
        print('select init')
        nextState = self._nextState()
        if nextState:
            return self.advance(nextState)
        else:
            self._context.setHelpString('select an object')
            self._waitForInput()
            return self

    def selectionChanged(self):
        print('select callback')
        nextState = self._nextState()
        if nextState:
            return self.advance(nextState)
        else:
            self._waitForInput()
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
        return DoNothing(self._context).init()

    def _waitForInput(self):
        self._context.unlisten()
        om.MGlobal.setSelectionMode(om.MGlobal.kSelectObjectMode)
        self._context.listen()

    def _nextState(self):
        selection = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection)

        if not selection.isEmpty():
            dagPath = om.MDagPath()
            selection.getDagPath(0, dagPath)
            print(dagPath.fullPathName())
            return SelectRootFace(self._context, dagPath)
        else:
            return None


class SelectRootFace(DoNothing):
    """ Select the root face for the face tree selection tool. """

    def __init__(self, context, dagPath):
        DoNothing.__init__(self, context)
        self._dagPath = dagPath
        self._dagPath.extendToShape()

    def init(self):
        print('root init')
        nextState = self._nextState()
        if nextState:
            print('gggg')
            return self.advance(nextState)
        else:
            self._context.setHelpString('select the root face')
            self._waitForInput()
            return self

    def selectionChanged(self):
        print('root callback')
        nextState = self._nextState()
        if nextState:
            print('kkk')
            return self.advance(nextState)
        else:
            self._waitForInput()
            return self

    def delete(self):
        print('root delete')
        return SelectObject(self._context)

    def complete(self):
        print('root complete')
        return self.abort()

    def abort(self):
        om.MGlobal.displayWarning('Nothing done.')
        self._context.unlisten()
        print('root abort')
        return DoNothing(self._context)

    def _waitForInput(self):
        self._context.unlisten()
        om.MGlobal.setSelectionMode(om.MGlobal.kSelectComponentMode)
        om.MGlobal.setComponentSelectionMask(om.MSelectionMask(om.MSelectionMask.kSelectMeshFaces))
        hiliteList = om.MSelectionList()
        hiliteList.add(self._dagPath)
        om.MGlobal.setActiveSelectionList(hiliteList)
        om.MGlobal.setHiliteList(hiliteList)
        self._context.listen()

    def _nextState(self):
        print('advance')
        selection = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection)
        if selection.length() != 1:
            print('list too long', selection.length())
            return None
        dagPath = om.MDagPath()
        components = om.MObject()
        selection.getDagPath(0, dagPath, components)

        if dagPath.node() != self._dagPath.node():
            print('nodes are not the same', dagPath.fullPathName(), self._dagPath.fullPathName())
            return None
        print(components.apiTypeStr())
        if not components.hasFn(om.MFn.kMeshPolygonComponent):
            print('wrong component type')
            return None

        faceIter = om.MItMeshPolygon(dagPath, components)
        if faceIter.isDone():
            print('face iter was done')
            return None

        print(faceIter.index())
        return SelectFacesInOrder(self._context, dagPath, faceIter.index())


class SelectFacesInOrder(DoNothing):
    """ Select faces in order. """

    def __init__(self, context, dagPath, rootFace):
        DoNothing.__init__(self, context)
        self._dagPath = dagPath
        self._rootFace = rootFace

    def init(self):
        print('order init')
        self._faces = []
        self._selectableFaces = None
        self._patchBuilder = MeshPatchBuilder()
        om.MGlobal.setSelectionMode(om.MGlobal.kSelectComponentMode)
        om.MGlobal.setComponentSelectionMask(om.MSelectionMask(om.MSelectionMask.kSelectMeshFaces))
        hiliteList = om.MSelectionList()
        hiliteList.add(self._dagPath)
        om.MGlobal.setActiveSelectionList(hiliteList)
        om.MGlobal.setHiliteList(hiliteList)
        self._context._setHelpString('Select faces in order')
        self._context.listen()
        return self

    def selectionChanged(self):
        self._context.unlisten()
        print('order evaluate')
        selection = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection)
        if not selection.length() is 0:
            print('order has selection')
            dagPath = om.MDagPath()
            components = om.MObject()
            selection.getDagPath(0, dagPath, components)
            faces = om.MIntArray()
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
        else:
            print('selection was empty')
        self._context.listen()
        return self

    def flatten(self):
        tree = createFacetreeSelectionOrder(self._dagPath, self._faces)
        self._patchBuilder.reset()
        flattenTree(self._dagPath, tree, self._patchBuilder)

    def delete(self):
        self._context.unlisten()
        if self._faces:
            self._faces.pop()
        self.flatten()
        self._selectFaces()
        self._context.listen()
        print('order delete')
        return self

    def complete(self):
        self._context.unlisten()
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
        self._state = SelectObject(self).init()

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

    def setHelpString(self, msg):
        self._setHelpString(msg)



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
