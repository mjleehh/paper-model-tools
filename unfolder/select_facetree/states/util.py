import maya.OpenMaya as om


def getEventPosition(event):
    xPos = om.MScriptUtil()
    xPos.createFromInt(0)
    xPosPtr = xPos.asShortPtr()
    yPos = om.MScriptUtil()
    yPos.createFromInt(2)
    yPosPtr = yPos.asShortPtr()
    event.getPosition(xPosPtr, yPosPtr)
    return (om.MScriptUtil(xPosPtr).asShort(), om.MScriptUtil(yPosPtr).asShort())

def getSelectedFace(dagPath):
        selection = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection)

        if selection.length() != 1:
            print('list too long', selection.length())
            return None

        selectionDagPath = om.MDagPath()
        components = om.MObject()
        selection.getDagPath(0, selectionDagPath, components)
        selectionDagPath.extendToShape()

        if selectionDagPath.node() != dagPath.node():
            print('nodes are not the same', selectionDagPath.fullPathName(), dagPath.fullPathName())
            return None

        if not components.hasFn(om.MFn.kMeshPolygonComponent):
            print('wrong component type')
            return None

        faceIter = om.MItMeshPolygon(selectionDagPath, components)
        if faceIter.isDone():
            om.MGlobal.displayWarning('selected face list was empty')
            return None

        if (faceIter.count() > 1):
            om.MGlobal.displayWarning('more than one face selected at once')

        face = faceIter.index()
        return face

def highlightFaces(dagPath, faces):
    print('highlightling')
    print(faces)
    faceComponents = om.MFnSingleIndexedComponent()
    faceComponents.create(om.MFn.kMeshPolygonComponent)
    for face in faces:
        faceComponents.addElement(face)

    selection = om.MSelectionList()
    selection.add(dagPath, faceComponents.object())
    hilite = om.MSelectionList()
    hilite.add(dagPath)
    print('setting selection')
    om.MGlobal.setSelectionMode(om.MGlobal.kSelectComponentMode)
    om.MGlobal.setComponentSelectionMask(om.MSelectionMask(om.MSelectionMask.kSelectMeshFaces))
    om.MGlobal.setActiveSelectionList(selection)
    om.MGlobal.setHiliteList(hilite)