import maya.OpenMaya as om

from .do_nothing import DoNothing
from .state import State
from .util import getEventPosition

from unfolder.create_patch.patch import flattenTree


class SelectStripRoot(State):

    def __init__(self, stateFactory, previous, dagPath, patchBuilder, facetree):
        print('add faces to strip init')
        State.__init__(self, stateFactory, previous)
        self._dagPath = dagPath
        self._facetree = facetree
        self._patchBuilder = patchBuilder

    def ffwd(self):
        self._waitForInput()
        return self

    def doPress(self, event):
        print('add faces do press')

        pos = getEventPosition(event)
        om.MGlobal.selectFromScreen(pos[0], pos[1], om.MGlobal.kReplaceList)

        return self._handleSelection()

    def flatten(self):
        self._patchBuilder.reset()
        flattenTree(self._dagPath, self._facetree, self._patchBuilder)

    def delete(self):
        return self

    def complete(self):
        print('order complete')
        return DoNothing(self._context)

    def abort(self):
        print('order abort')
        return DoNothing(self._context)

    def _helpString(self):
        return 'select faces from strip in order'

    def _handleSelection(self):
        selectedFace = self._getSelectedFace()
        if selectedFace:
            faceNode = self._facetree.findSubtree(selectedFace)
            return self._stateFactory.addFacesToStrip(None, self._dagPath, self._patchBuilder, faceNode)()
        else:
            return self

    def _waitForInput(self):
        self._updateSelectableFaces()
        self._hightlightSelectableFaces()

    def _hightlightSelectableFaces(self):
        print('highlightling')
        print(self._selectableFaces)
        faceComponents = om.MFnSingleIndexedComponent()
        faceComponents.create(om.MFn.kMeshPolygonComponent)
        for face in self._selectableFaces:
            faceComponents.addElement(face)

        selection = om.MSelectionList()
        selection.add(self._dagPath, faceComponents.object())
        hilite = om.MSelectionList()
        hilite.add(self._dagPath)
        print('setting selection')
        om.MGlobal.setSelectionMode(om.MGlobal.kSelectComponentMode)
        om.MGlobal.setComponentSelectionMask(om.MSelectionMask(om.MSelectionMask.kSelectMeshFaces))
        om.MGlobal.setActiveSelectionList(selection)
        om.MGlobal.setHiliteList(hilite)

    def _updateSelectableFaces(self):
        self._selectableFaces = self._facetree.getFaces()


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