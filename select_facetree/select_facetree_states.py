class DoNothing():
    """ Final state of the face tree selection tool.

        Do nothing on input. When the context has been completed it remains in
        this state.
    """
    def __init__(self, context):
        self._context = context

    def init(self):
        self._context.listen()
        self._context.setHelpString('face tree selection tool done')
        return self

    def advance(self, nextState):
        print('advance')
        self._context.unlisten()
        return nextState.init()

    def selectionChanged(self):
        print('nothing callback')
        return self

    def delete(self):
        print('nothing delete')
        return self

    def complete(self):
        print('nothing complete')
        return self

    def abort(self):
        print('nothing abort')
        return self


class SelectObject(DoNothing):
    """ Select an object for the face tree selection tool. """

    def __init__(self, context):
        DoNothing.__init__(self, context)

    def init(self):
        print('select init')
        nextState = self._nextState()
        if nextState:
            return self.advance(nextState)
        else:
            self._context.setHelpString('select an object')
            self._waitForInput()
            return self

    def selectionChanged(self):
        print('select callback')
        nextState = self._nextState()
        if nextState:
            return self.advance(nextState)
        else:
            self._waitForInput()
            return self

    def delete(self):
        print('select delete')
        return self.abort()

    def complete(self):
        print('select complete')
        return self.abort()

    def abort(self):
        om.MGlobal.displayWarning('Nothing done.')
        self._context.unlisten()
        print('select abort')
        return DoNothing(self._context).init()

    def _waitForInput(self):
        self._context.unlisten()
        om.MGlobal.setSelectionMode(om.MGlobal.kSelectObjectMode)
        self._context.listen()

    def _nextState(self):
        selection = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection)

        if not selection.isEmpty():
            dagPath = om.MDagPath()
            selection.getDagPath(0, dagPath)
            print(dagPath.fullPathName())
            return SelectFace(self._context, dagPath)
        else:
            return None


class SelectFace(DoNothing):
    """ Select the root face for the face tree selection tool. """

    def __init__(self, context, dagPath):
        DoNothing.__init__(self, context)
        self._dagPath = dagPath
        self._dagPath.extendToShape()
        if context.factree:
            self.selectableFaces = context.factree.getFaces()
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
        return SelectObject(self._context)

    def complete(self):
        print('root complete')
        return self.abort()

    def abort(self):
        om.MGlobal.displayWarning('Nothing done.')
        self._context.unlisten()
        print('root abort')
        return DoNothing(self._context)

    def _waitForInput(self):
        self._context.unlisten()
        om.MGlobal.setSelectionMode(om.MGlobal.kSelectComponentMode)
        om.MGlobal.setComponentSelectionMask(om.MSelectionMask(om.MSelectionMask.kSelectMeshFaces))
        hiliteList = om.MSelectionList()
        hiliteList.add(self._dagPath)
        om.MGlobal.setActiveSelectionList(hiliteList)
        om.MGlobal.setHiliteList(hiliteList)
        self._context.listen()

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

        if dagPath.node() != self._dagPath.node():
            print('nodes are not the same', dagPath.fullPathName(), self._dagPath.fullPathName())
            return None
        print(components.apiTypeStr())
        if not components.hasFn(om.MFn.kMeshPolygonComponent):
            print('wrong component type')
            return None

        faceIter = om.MItMeshPolygon(dagPath, components)
        if faceIter.isDone():
            om.MGlobal.displayWarning("selected face list was empty")
            return None

        if (faceIter.count() > 1):
            om.MGlobal.displayWarning("more than one face selected at once")

        face = faceIter.index()
        if self.selectableFaces and face not in self.selectableFaces:
            return None
        return face

    def _nextState(self):
        selectedFace = self._getSelectedFace()
        if selectedFace:
            return AddFacesToStrip(self._context, self._dagPath, )
        else:
            return None

class AddFacesToStrip(DoNothing):
    def __init__(self, context, initialNode):
        DoNothing.__init_(context)
        self._initialNode = initialNode






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
        self._context.listen()
        return self

    def selectionChanged(self):
        self._context.unlisten()
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
        self._context.listen()
        return self

    def flatten(self):
        tree = createFacetreeSelectionOrder(self._dagPath, self._faces)
        self._patchBuilder.reset()
        flattenTree(self._dagPath, tree, self._patchBuilder)

    def delete(self):
        self._context.unlisten()
        if self._faces:
            self._faces.pop()
        self.flatten()
        self._selectFaces()
        self._context.listen()
        print('order delete')
        return self

    def complete(self):
        self._context.unlisten()
        self.flatten()
        print('order complete')
        return self.abort()

    def abort(self):
        self._context.unlisten()
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
