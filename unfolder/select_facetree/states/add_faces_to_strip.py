import maya.OpenMaya as om

from .do_nothing import DoNothing
from .state import State
from .util import getEventPosition

from unfolder.create_patch.patch import flattenTree
from unfolder.util.helpers import setIter


class AddFacesToStrip(State):

    def __init__(self, stateFactory, previous, dagPath, patchBuilder, stripRoot):
        print('add faces to strip init')
        State.__init__(self, stateFactory, previous)
        self._dagPath = dagPath
        self._currentNode = stripRoot
        self._facetree = stripRoot.getRoot()
        self._updateSelectableFaces()
        self._patchBuilder = patchBuilder

    def ffwd(self):
        self._waitForInput()
        return self

    def doPress(self, event):
        print('add faces do press')

        pos = getEventPosition(event)
        om.MGlobal.selectFromScreen(pos[0], pos[1], om.MGlobal.kReplaceList)

        return self._handleSelection()

    def _handleSelection(self):
        selection = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection)
        if not selection.length() is 0:
            print('add faces has selection')
            dagPath = om.MDagPath()
            components = om.MObject()
            selection.getDagPath(0, dagPath, components)
            faceIter = om.MItMeshPolygon(dagPath, components)
            face = faceIter.index()
            faces = []
            while not faceIter.isDone():
                faces.append(faceIter.index())
                faceIter.next()

            if face in self._selectableFaces:
                self._currentNode = self._currentNode.addChild(face)
        else:
            print('selection was empty')
        self._waitForInput()
        return self

    def flatten(self):
        self._patchBuilder.reset()
        flattenTree(self._dagPath, self._facetree, self._patchBuilder)

    def delete(self):
        return self

    def complete(self):
        print('order complete')
        return self._stateFactory.selectStripRoot(None, self._dagPath, self._patchBuilder, self._facetree)()

    def abort(self):
        print('order abort')
        return DoNothing(self._context)

    def _helpString(self):
        return 'select faces from strip in order'

    def _waitForInput(self):
        self._updateSelectableFaces()
        self._hightlightSelectableFaces()
        self.flatten()

    def _hightlightSelectableFaces(self):
        print('highlightling')
        print(self._selectableFaces)
        faceComponents = om.MFnSingleIndexedComponent()
        faceComponents.create(om.MFn.kMeshPolygonComponent)
        for face in self._selectableFaces:
            faceComponents.addElement(face)

        selection = om.MSelectionList()
        selection.add(self._dagPath, faceComponents.object())
        hilite = om.MSelectionList()
        hilite.add(self._dagPath)
        print('setting selection')
        om.MGlobal.setSelectionMode(om.MGlobal.kSelectComponentMode)
        om.MGlobal.setComponentSelectionMask(om.MSelectionMask(om.MSelectionMask.kSelectMeshFaces))
        om.MGlobal.setActiveSelectionList(selection)
        om.MGlobal.setHiliteList(hilite)

    def _updateSelectableFaces(self):
        print('updateing selectable')
        faceIter = om.MItMeshPolygon(self._dagPath)
        setIter(faceIter, self._currentNode.face)
        connectedFaces = om.MIntArray()
        faceIter.getConnectedFaces(connectedFaces)
        print('determine selectables')
        print(list(connectedFaces))
        print(list(self._facetree.getFaces()))
        print(frozenset(connectedFaces) - frozenset(self._facetree.getFaces()))
        self._selectableFaces = frozenset(connectedFaces) - frozenset(self._facetree.getFaces())
