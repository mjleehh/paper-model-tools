import maya.OpenMaya as om
from .do_nothing import DoNothing
from .select_face import SelectFace


class SelectObject(DoNothing):
    """ Select an object for the face tree selection tool. """

    def __init__(self, context):
        self._context = context

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
        print('select abort')
        return DoNothing(self._context).init()

    def _waitForInput(self):
        om.MGlobal.setSelectionMode(om.MGlobal.kSelectObjectMode)

    def _nextState(self):
        selection = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection)

        if not selection.isEmpty():
            dagPath = om.MDagPath()
            selection.getDagPath(0, dagPath)
            print(dagPath.fullPathName())
            return SelectFace(self._context, dagPath, None)
        else:
            return None

def create(context):
    return SelectObject(context).init()
