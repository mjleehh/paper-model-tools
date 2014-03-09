import maya.OpenMaya as om
import maya.OpenMayaMPx as omp

from unfolder.util.selection import Selection
from .states.initial_state import createInitialState

class SelectFacetreeContext(omp.MPxSelectionContext):
    def __init__(self):
        omp.MPxSelectionContext.__init__(self)
        self._state = None
        self._callback = None
        self._selection = None

    def toolOnSetup(self, event):
        """ Called each time the context is activated. """
        self._selection = Selection()
        self._state = createInitialState(self)
        self._listen()

    def toolOffCleanup(self):
        """ Called each time the context is deactivated. """
        self._unlisten()
        if self._selection:
            self._selection.makeCurrent()
            self._selection = None
        self._state = None
        print('cleanup')
        self._unlisten()

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

    def setHelpString(self, msg):
        self._setHelpString(msg)

    def _doCallback(self, f):
        self._unlisten()
        self._state = f()
        self._listen()

    def _listen(self):
        """ Enable callback for selection changes. """
        print('LISTEN')
        print('UNLISTEN LAST')
        self._unlisten()
        print('LISTEN NEW')
        self._callback = om.MModelMessage.addCallback(om.MModelMessage.kActiveListModified, selectionChanged, self)

    def _unlisten(self):
        """ Disable callback for selection changes. """
        print('UNLISTEN')
        if self._callback:
                om.MModelMessage.removeCallback(self._callback)
                self._callback = None


def selectionChanged(context):
    """ Callback for selection changes.

    Delegates handling to context instance. """
    context.selectionChanged()
