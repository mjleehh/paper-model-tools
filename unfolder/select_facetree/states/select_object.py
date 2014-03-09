import maya.OpenMaya as om

from .select_face import SelectFace
from .do_nothing import DoNothing

from unfolder.select_facetree.states.util import getEventPosition


class SelectObject(DoNothing):
    """ Select an object for the face tree selection tool. """

    def __init__(self, context):
        self._context = context
        self._previous = self.reset

    def ffwd(self):
        print('select init')

        nextState = self._nextState()
        if nextState:
            return nextState()
        else:
            return self.reset()

    def reset(self):
        self._context.setHelpString('select an object to unfold')
        self._waitForInput()
        return self

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
        return DoNothing(self._context).ffwd()

    def _waitForInput(self):
        om.MGlobal.setSelectionMode(om.MGlobal.kSelectObjectMode)
        om.MGlobal.setActiveSelectionList(om.MSelectionList())

    def _nextState(self):
        selection = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection)

        if not selection.isEmpty():
            dagPath = om.MDagPath()
            selection.getDagPath(0, dagPath)
            print(dagPath.fullPathName())
            return SelectFace(self._context, self.reset, dagPath, None).ffwd
        else:
            return None

