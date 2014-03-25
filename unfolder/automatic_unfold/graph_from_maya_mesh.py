from unfolder.util.mesh_faces import MeshFaces, indices, index


def convertMayaMeshToGraph(dagPath, faceIndices, graphBuilder):

    faces = MeshFaces(dagPath, faceIndices)

    for face in faces:
        connectedFaceIndices = indices(face.getConnectedFaces())
        graphBuilder.addNode(index(face), connectedFaceIndices)

    return graphBuilder.toGraph()