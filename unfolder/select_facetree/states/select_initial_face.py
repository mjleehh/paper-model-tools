import maya.OpenMaya as om

from .add_faces_to_strip import AddFacesToStrip
from .state import State
from .do_nothing import DoNothing
from unfolder.create_patch.patch_builder import MeshPatchBuilder

from unfolder.facetree import Node
from unfolder.select_facetree.states.util import getEventPosition


class SelectInitialFace(State):
    """ Select the root face for the face tree selection tool. """

    def __init__(self, stateFactory, previous, dagPath):
        State.__init__(self, stateFactory, previous)
        self._dagPath = dagPath
        self._dagPath.extendToShape()

    # event callbacks

    def delete(self):
        print('root delete')
        return self._previous()

    def abort(self):
        om.MGlobal.displayWarning('Nothing done.')
        print('root abort')
        return self._stateFactory.doNothing()()

    def _helpString(self):
        return 'select a root face for patch'

    # advance

    def doPress(self, event):
        print('root do press')
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
        selectedFace = self._getSelectedFace()
        if selectedFace:
            return self._stateFactory.addFacesToStrip(self.reset, self._dagPath, MeshPatchBuilder(), Node(selectedFace))
        else:
            return None

    def _getSelectedFace(self):
        print('advance')
        selection = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection)
        if selection.length() != 1:
            print('list too long', selection.length())
            return None
        dagPath = om.MDagPath()
        components = om.MObject()
        selection.getDagPath(0, dagPath, components)
        dagPath.extendToShape()

        if dagPath.node() != self._dagPath.node():
            print('nodes are not the same', dagPath.fullPathName(), self._dagPath.fullPathName())
            return None
        print(components.apiTypeStr())
        if not components.hasFn(om.MFn.kMeshPolygonComponent):
            print('wrong component type')
            return None

        faceIter = om.MItMeshPolygon(dagPath, components)
        if faceIter.isDone():
            om.MGlobal.displayWarning('selected face list was empty')
            return None

        if (faceIter.count() > 1):
            om.MGlobal.displayWarning('more than one face selected at once')

        face = faceIter.index()
        return face