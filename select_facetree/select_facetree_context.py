import maya.OpenMayaMPx as omp

from unfolder.util.selection import Selection
from unfolder.select_facetree.select_facetree_states import SelectObject


class SelectFacetreeContext(omp.MPxSelectionContext):
    def __init__(self):
        omp.MPxSelectionContext.__init__(self)
        self._state = None
        self._callback = None
        self._selection = None
        self.facetree = None

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