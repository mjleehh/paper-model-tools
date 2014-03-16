import maya.OpenMaya as om
import maya.OpenMayaMPx as omp

from unfolder.util.selection import Selection

class SelectFacetreeContext(omp.MPxSelectionContext):
    def __init__(self, stateFactory):
        omp.MPxSelectionContext.__init__(self)
        self._stateFactory = stateFactory
        self._state = None
        self._callback = None
        self._listening = False
        self._selection = None

    def toolOnSetup(self, event):
        """ Called each time the context is activated. """
        print('setting up tool')
        self._selection = Selection()
        self._state = self._stateFactory.initialState()
        self._state = self._state()
        self._setHelpString(self._state.helpString())

    def toolOffCleanup(self):
        """ Called each time the context is deactivated. """
        if self._selection:
            self._selection.makeCurrent()
            self._selection = None
        self._state = None
        print('tool cleanup completed')

    # callbacks

    def doPress(self, event):
        self._doCallback(self._state.doPress, event)

    def doDrag(self, event):
        self._doCallback(self._state.doDrag, event)

    def doRelease(self, event):
        self._doCallback(self._state.doRelease, event)

    def completeAction(self):
        """ Complete the tool (enter has been pressed). """
        self._doCallback(self._state.complete)

    def deleteAction(self):
        """ Go one step back (backspace has been pressed). """
        self._doCallback(self._state.delete)

    def abortAction(self):
        """ Abort the tool (escape has been pressed). """
        self._doCallback(self._state.abort)

    def selectionChanged(self):
        """ Called when the selection has changed. """
        print('selection changed context')
        self._doCallback(self._state.selectionChanged)

    def _doCallback(self, f, *args):
        self._state = f(*args)
        self._setHelpString(self._state.helpString())
