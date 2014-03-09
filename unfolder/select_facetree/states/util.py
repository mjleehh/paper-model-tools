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
