from unfolder.graph.graph import Graph


def meshToGraph(faces, graphBuilder) -> Graph:

    for face in faces:
        connectedFaceIndices = face.getConnectedFaces().indices
        graphBuilder.addNode(face.index, connectedFaceIndices)
    return Graph(graphBuilder.toGraph())