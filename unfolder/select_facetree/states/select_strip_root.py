import maya.OpenMaya as om

from .do_nothing import DoNothing
from .state import State
from .util import getEventPosition, getSelectedFace, highlightFaces

from unfolder.create_patch.patch import flattenTree


class SelectStripRoot(State):

    def __init__(self, stateFactory, previous, dagPath, patchBuilder, facetree):
        State.__init__(self, stateFactory, previous)
        self._dagPath = dagPath
        self._facetree = facetree
        self._patchBuilder = patchBuilder

    def helpString(self):
        return 'select a face to begin a new strip'

    def ffwd(self):
        self._waitForInput()
        return self

    def doPress(self, event):
        pos = getEventPosition(event)
        om.MGlobal.selectFromScreen(pos[0], pos[1], om.MGlobal.kReplaceList)

        return self._handleSelection()

    def flatten(self):
        self._patchBuilder.reset()
        flattenTree(self._dagPath, self._facetree, self._patchBuilder)

    def delete(self):
        return self

    def complete(self):
        return DoNothing()

    def abort(self):
        return DoNothing()

    def _handleSelection(self):
        selectedFace = getSelectedFace(self._dagPath)
        if selectedFace:
            faceNode = self._facetree.findSubtree(selectedFace)
            return self._stateFactory.addFacesToStrip(None, self._dagPath, self._patchBuilder, faceNode)()
        else:
            return self

    def _waitForInput(self):
        self._updateSelectableFaces()
        highlightFaces(self._dagPath, self._selectableFaces)

    def _updateSelectableFaces(self):
        self._selectableFaces = self._facetree.getFaces()
