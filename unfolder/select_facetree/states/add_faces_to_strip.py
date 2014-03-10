import maya.OpenMaya as om

from .do_nothing import DoNothing
from unfolder.create_patch.patch import flattenTree
from unfolder.create_patch.patch_builder import MeshPatchBuilder
from .state import State
from .util import getEventPosition
from unfolder.util.helpers import setIter


class AddFacesToStrip(State):

    def __init__(self, context, previous, dagPath, initialNode, facetree):
        print('add faces to strip init')
        State.__init__(self, context, previous)
        self._dagPath = dagPath
        self._currentNode = initialNode
        self._facetree = facetree
        self._patchBuilder = MeshPatchBuilder()


    def doPress(self, event):
        print('add faces do press')

        pos = getEventPosition(event)
        om.MGlobal.selectFromScreen(pos[0], pos[1], om.MGlobal.kReplaceList)

        return self.ffwd()

    def _nextState(self):
        selection = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection)
        if not selection.length() is 0:
            print('add faces has selection')
            dagPath = om.MDagPath()
            components = om.MObject()
            selection.getDagPath(0, dagPath, components)
            faceIter = om.MItMeshPolygon(dagPath, components)
            face = faceIter.index()
            faces = []
            while not faceIter.isDone():
                faces.append(faceIter.index())
                faceIter.next()

            if face in self._selectableFaces:
                print('current    ' + str(self._currentNode.face))
                self._currentNode = self._currentNode.addChild(face)
                self.flatten()
                print('sel        ' + str(faces))
                print('selectable ' + str(self._selectableFaces))
                print("tree       " + str(self._facetree.getFaces()))
                self._updateSelectableFaces()
        else:
            print('selection was empty')
        self._hightlightSelectableFaces()
        return self

    def flatten(self):
        self._patchBuilder.reset()
        flattenTree(self._dagPath, self._facetree, self._patchBuilder)

    def delete(self):
        return self

    def complete(self):
        self.flatten()
        print('order complete')
        return self.abort()

    def abort(self):
        print('order abort')
        return DoNothing(self._context)

    def _helpString(self):
        return 'select faces from strip in order'

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
        print('updateing selectable')
        faceIter = om.MItMeshPolygon(self._dagPath)
        setIter(faceIter, self._currentNode.face)
        connectedFaces = om.MIntArray()
        faceIter.getConnectedFaces(connectedFaces)
        print('determine selectables')
        print(list(connectedFaces))
        print(list(self._facetree.getFaces()))
        print(frozenset(connectedFaces) - frozenset(self._facetree.getFaces()))
        self._selectableFaces = frozenset(connectedFaces) - frozenset(self._facetree.getFaces())
