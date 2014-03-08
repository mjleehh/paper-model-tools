import maya.OpenMaya as om

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