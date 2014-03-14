import maya.OpenMaya as om

from .state import State

from unfolder.select_facetree.states.util import getEventPosition


class SelectObject(State):
    """ Select an object for the face tree selection tool. """

    def __init__(self, stateFactory):
        State.__init__(self, stateFactory, None)

    # event callbacks

    def doPress(self, event):
        print('select do press')

        pos = getEventPosition(event)
        om.MGlobal.selectFromScreen(pos[0], pos[1], om.MGlobal.kReplaceList, om.MGlobal.kSurfaceSelectMethod)
        return self.ffwd()

    def delete(self):
        print('select delete')
        return self.abort()

    def complete(self):
        print('select complete')
        return self.abort()

    def abort(self):
        om.MGlobal.displayWarning('Nothing done.')
        print('select abort')
        return self._stateFactory.doNoting()()

    def _helpString(self):
        return 'select an object to unfold'

    def _waitForInput(self):
        emptySelection = om.MSelectionList()
        om.MGlobal.setSelectionMode(om.MGlobal.kSelectObjectMode)
        om.MGlobal.setActiveSelectionList(emptySelection)
        om.MGlobal.setHiliteList(emptySelection)

    def _nextState(self):
        selection = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection)

        if not selection.isEmpty():
            dagPath = om.MDagPath()
            selection.getDagPath(0, dagPath)
            print(dagPath.fullPathName())
            return self._stateFactory.selectInitialFace(self.reset, dagPath)
        else:
            return None

