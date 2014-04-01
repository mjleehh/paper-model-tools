def indices(meshComponentList):
    return [component.index for component in meshComponentList]

def meshToGraph(faces, graphBuilder):

    for face in faces:
        connectedFaceIndices = indices(face.getConnectedFaces())
        graphBuilder.addNode(face.index, connectedFaceIndices)

    return graphBuilder.toGraph()