import maya.OpenMaya as om

from .do_nothing import DoNothing
from .state import State
from .util import getEventPosition, getSelectedFace, highlightFaces

from unfolder.create_patch.patch import flattenTree
from unfolder.util.helpers import setIter


class AddFacesToStrip(State):

    def __init__(self, stateFactory, previous, dagPath, patchBuilder, stripRoot):
        State.__init__(self, stateFactory, previous)
        self._dagPath = dagPath
        self._currentNode = stripRoot
        self._facetree = stripRoot.getRoot()
        self._updateSelectableFaces()
        self._patchBuilder = patchBuilder

    def helpString(self):
        return 'select faces for strip in order'

    # event callbacks

    def delete(self):
        node = self._currentNode.remove()
        if node:
            self._currentNode = node
            self._waitForInput()
            return self
        else:
            return self._previous()

    def complete(self):
        return self._stateFactory.selectStripRoot(None, self._dagPath, self._patchBuilder, self._facetree)()

    def abort(self):
        return DoNothing()

    # advance

    def ffwd(self):
        self._waitForInput()
        return self

    def doPress(self, event):
        pos = getEventPosition(event)
        om.MGlobal.selectFromScreen(pos[0], pos[1], om.MGlobal.kReplaceList)

        selectedFace = getSelectedFace(self._dagPath)
        if selectedFace in self._selectableFaces:
            self._currentNode = self._currentNode.addChild(selectedFace)

        self._waitForInput()
        return self

    def flatten(self):
        self._patchBuilder.reset()
        flattenTree(self._dagPath, self._facetree, self._patchBuilder)

    def _waitForInput(self):
        self._updateSelectableFaces()
        highlightFaces(self._dagPath, self._selectableFaces)
        self.flatten()

    def _updateSelectableFaces(self):
        faceIter = om.MItMeshPolygon(self._dagPath)
        setIter(faceIter, self._currentNode.face)
        connectedFaces = om.MIntArray()
        faceIter.getConnectedFaces(connectedFaces)
        self._selectableFaces = frozenset(connectedFaces) - frozenset(self._facetree.getFaces())
