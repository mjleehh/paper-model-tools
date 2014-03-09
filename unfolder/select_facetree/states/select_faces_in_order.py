import maya.OpenMaya as om

from .do_nothing import DoNothing
from unfolder.create_patch.patch_builder import MeshPatchBuilder


class SelectFacesInOrder(DoNothing):
    """ Select faces in order. """

    def __init__(self, context, dagPath, rootFace):
        DoNothing.__init__(self, context)
        self._dagPath = dagPath
        self._rootFace = rootFace
        self._faces = [rootFace]
        self._selectableFaces = None
        self._patchBuilder = MeshPatchBuilder()

    def init(self):
        print('order init')
        om.MGlobal.setSelectionMode(om.MGlobal.kSelectComponentMode)
        om.MGlobal.setComponentSelectionMask(om.MSelectionMask(om.MSelectionMask.kSelectMeshFaces))
        hiliteList = om.MSelectionList()
        hiliteList.add(self._dagPath)
        om.MGlobal.setActiveSelectionList(hiliteList)
        om.MGlobal.setHiliteList(hiliteList)
        self._selectFaces()
        self._context.setHelpString('Select faces in order')
        self._context._listen()
        return self

    def selectionChanged(self):
        self._context._unlisten()
        print('order evaluate')
        selection = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection)
        if not selection.length() is 0:
            print('order has selection')
            dagPath = om.MDagPath()
            components = om.MObject()
            selection.getDagPath(0, dagPath, components)
            faces = om.MIntArray()
            a = om.MFnSingleIndexedComponent(components)
            a.getElements(faces)

            newFaces = frozenset(faces) - frozenset(self._faces)
            if self._selectableFaces:
                newFaces = newFaces & self._selectableFaces
            self._faces.extend(newFaces)
            print('faces: ' + str(self._faces))
            print('new faces ' + str(newFaces))

            self.flatten()
            self._selectFaces()
        else:
            print('selection was empty')
        self._context._listen()
        return self

    def flatten(self):
        tree = createFacetreeSelectionOrder(self._dagPath, self._faces)
        self._patchBuilder.reset()
        flattenTree(self._dagPath, tree, self._patchBuilder)

    def delete(self):
        self._context._unlisten()
        if self._faces:
            self._faces.pop()
        self.flatten()
        self._selectFaces()
        self._context._listen()
        print('order delete')
        return self

    def complete(self):
        self._context._unlisten()
        self.flatten()
        print('order complete')
        return self.abort()

    def abort(self):
        self._context._unlisten()
        print('order abort')
        return DoNothing(self._context)

    def _selectFaces(self):
        faceComponents = om.MFnSingleIndexedComponent()
        faceComponents.create(om.MFn.kMeshPolygonComponent)
        for face in self._faces:
            faceComponents.addElement(face)

        selection = om.MSelectionList()
        selection.add(self._dagPath, faceComponents.object())
        om.MGlobal.setActiveSelectionList(selection)
        self._updateSelectableFaces(faceComponents)

    def _updateSelectableFaces(self, faceComponents):
        if self._faces:
            allConnectedFaces = []
            faceIter = om.MItMeshPolygon(self._dagPath, faceComponents.object())
            while not faceIter.isDone():
                connectedFaces = om.MIntArray()
                faceIter.getConnectedFaces(connectedFaces)
                allConnectedFaces.extend(connectedFaces)
                faceIter.next()
                self._selectableFaces = frozenset(allConnectedFaces)
