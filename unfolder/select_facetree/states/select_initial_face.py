import maya.OpenMaya as om

from .add_faces_to_strip import AddFacesToStrip
from .state import State
from .do_nothing import DoNothing
from unfolder.create_patch.patch_builder import MeshPatchBuilder

from unfolder.facetree import Node
from unfolder.select_facetree.states.util import getEventPosition, \
    getSelectedFace


class SelectInitialFace(State):
    """ Select the root face for the face tree selection tool. """

    def __init__(self, stateFactory, previous, dagPath):
        State.__init__(self, stateFactory, previous)
        self._dagPath = dagPath
        self._dagPath.extendToShape()

    def helpString(self):
        return 'select a first face'

    # event callbacks

    def abort(self):
        om.MGlobal.displayWarning('Nothing done.')
        return self._stateFactory.doNothing()()

    # advance

    def doPress(self, event):
        pos = getEventPosition(event)
        om.MGlobal.selectFromScreen(pos[0], pos[1], om.MGlobal.kReplaceList, om.MGlobal.kSurfaceSelectMethod)
        return self.ffwd()

    def _waitForInput(self):
        faceComponents = om.MFnSingleIndexedComponent()
        faceComponents.create(om.MFn.kMeshPolygonComponent)

        selection = om.MSelectionList()
        selection.add(self._dagPath)

        om.MGlobal.setSelectionMode(om.MGlobal.kSelectComponentMode)
        om.MGlobal.setComponentSelectionMask(om.MSelectionMask(om.MSelectionMask.kSelectMeshFaces))
        om.MGlobal.setActiveSelectionList(selection)
        om.MGlobal.setHiliteList(selection)

    def _nextState(self):
        selectedFace = getSelectedFace(self._dagPath)
        if selectedFace:
            return self._stateFactory.addFacesToStrip(self.reset, self._dagPath, MeshPatchBuilder(), Node(selectedFace))
        else:
            return None
