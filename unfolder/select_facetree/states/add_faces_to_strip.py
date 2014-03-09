import maya.OpenMaya as om

from .do_nothing import DoNothing
from unfolder.create_patch.patch import flattenTree
from unfolder.create_patch.patch_builder import MeshPatchBuilder
from unfolder.util.helpers import setIter


class AddFacesToStrip(DoNothing):

    def __init__(self, context, dagPath, initialNode, facetree):
        print('add faces to strip init')
        DoNothing.__init__(self, context)
        self._dagPath = dagPath
        self._currentNode = initialNode
        self._facetree = facetree
        self._patchBuilder = MeshPatchBuilder()

    def init(self):
        print('add faces init')
        om.MGlobal.setSelectionMode(om.MGlobal.kSelectComponentMode)
        om.MGlobal.setComponentSelectionMask(om.MSelectionMask(om.MSelectionMask.kSelectMeshFaces))
        hiliteList = om.MSelectionList()
        hiliteList.add(self._dagPath)
        om.MGlobal.setActiveSelectionList(hiliteList)
        om.MGlobal.setHiliteList(hiliteList)
        self._updateSelectableFaces()
        self._hightlightSelectableFaces()
        self._context.setHelpString('select faces from strip in order')
        return self

    def selectionChanged(self):
        print('add faces evaluate')
        selection = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection)
        if not selection.length() is 0:
            print('add faces has selection')
            dagPath = om.MDagPath()
            components = om.MObject()
            selection.getDagPath(0, dagPath, components)
            faceIter = om.MItMeshPolygon(dagPath, components)
            face = faceIter.index()

            faces = [face]
            while not faceIter.isDone():
                faces.append(faceIter.index())
                faceIter.next()
            print('selected faces ' + str(faces))

            if face in self._selectableFaces:
                self._currentNode = self._currentNode.addChild(face)
                self.flatten()
                self._updateSelectableFaces()
                print('sel        ' + str(face))
                print('selectable ' + str(self._selectableFaces))
                print("tree       " + str(self._facetree.getFaces()))
        else:
            print('selection was empty')
        #self._hightlightSelectableFaces()
        return self

    def flatten(self):
        self._patchBuilder.reset()
        flattenTree(self._dagPath, self._facetree, self._patchBuilder)

    def complete(self):
        self.flatten()
        print('order complete')
        return self.abort()

    def abort(self):
        print('order abort')
        return DoNothing(self._context)

    def _hightlightSelectableFaces(self):
        print('highlightling')
        faceComponents = om.MFnSingleIndexedComponent()
        faceComponents.create(om.MFn.kMeshPolygonComponent)
        for face in self._selectableFaces:
            faceComponents.addElement(face)

        selection = om.MSelectionList()
        selection.add(self._dagPath, faceComponents.object())
        om.MGlobal.setActiveSelectionList(selection)

    def _updateSelectableFaces(self):
        print('updateing selectable')
        faceIter = om.MItMeshPolygon(self._dagPath)
        setIter(faceIter, self._currentNode.face)
        connectedFaces = om.MIntArray()
        faceIter.getConnectedFaces(connectedFaces)
        self._selectableFaces = frozenset(connectedFaces) - frozenset(self._facetree.getFaces())
