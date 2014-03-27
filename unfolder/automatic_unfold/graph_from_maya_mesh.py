from unfolder.mesh.maya_mesh import indices, index


def graphFromFaces(faces, graphBuilder):

    for face in faces:
        connectedFaceIndices = indices(face.getConnectedFaces())
        graphBuilder.addNode(index(face), connectedFaceIndices)

    return graphBuilder.toGraph()