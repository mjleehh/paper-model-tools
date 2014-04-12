def meshToGraph(faces, graphBuilder):

    for face in faces:
        connectedFaceIndices = face.getConnectedFaces().indices
        graphBuilder.addNode(face.index, connectedFaceIndices)

    return graphBuilder.toGraph()