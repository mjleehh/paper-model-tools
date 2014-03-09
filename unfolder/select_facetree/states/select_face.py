import maya.OpenMaya as om

from unfolder.facetree import Node
from .add_faces_to_strip import AddFacesToStrip
from .do_nothing import DoNothing


class SelectFace(DoNothing):
    """ Select the root face for the face tree selection tool. """

    def __init__(self, context, dagPath, facetree):
        DoNothing.__init__(self, context)
        self._dagPath = dagPath
        self._dagPath.extendToShape()
        self._facetree = facetree
        if facetree:
            self.selectableFaces = facetree.getFaces()
        else:
            self.selectableFaces = None

    def init(self):
        print('root init')
        nextState = self._nextState()
        if nextState:
            return self.advance(nextState)
        else:
            self._context.setHelpString('select a root face for patch')
            self._waitForInput()
            return self

    def selectionChanged(self):
        print('root callback')
        nextState = self._nextState()
        if nextState:
            return self.advance(nextState)
        else:
            self._waitForInput()
            return self

    def delete(self):
        print('root delete')
        #return SelectObject(self._context)

    def complete(self):
        print('root complete')
        return self.abort()

    def abort(self):
        om.MGlobal.displayWarning('Nothing done.')
        print('root abort')
        return DoNothing(self._context)

    def _waitForInput(self):
        om.MGlobal.setSelectionMode(om.MGlobal.kSelectComponentMode)
        om.MGlobal.setComponentSelectionMask(om.MSelectionMask(om.MSelectionMask.kSelectMeshFaces))
        hiliteList = om.MSelectionList()
        hiliteList.add(self._dagPath)
        om.MGlobal.setActiveSelectionList(hiliteList)
        om.MGlobal.setHiliteList(hiliteList)

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
        if self.selectableFaces and face not in self.selectableFaces:
            return None
        return face

    def _nextState(self):
        selectedFace = self._getSelectedFace()
        if selectedFace:
            if self._facetree:
                initialNode = self._facetree.findSubtree(selectedFace)
                if not initialNode:
                    om.MGlobal.displayError('face tree is corrupted')
                    return None
                return AddFacesToStrip(self._context, self._dagPath, initialNode, self._facetree)
            else:
                facetree = Node(selectedFace)
                return AddFacesToStrip(self._context, self._dagPath, facetree, facetree)
        else:
            return None