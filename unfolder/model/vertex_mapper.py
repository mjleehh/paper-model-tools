from unfolder.util.plane_coordinate_system import PlaneCoordinateSystem


class VertexMapper:
    """ Determine the 2D coordinate system for one of the face edges

        The 2d coordinate system spans the face plane:
        - the origin is the first vertex of the edge
        - the first unit vector is the normalized vector from the first edge
          vertex to the second edge vertex
        - the second unit vector is the normalized vector directed at n x e_1

        Faces in maya have counter clockwise vertex order. Thus e_2 faces
        'into' the face area. The three vectors (e_1, e_2, n) for right handed
        coordinates for the 3D space (e_1 x e_2 = n).
    """
    def __init__(self, faceNormal, inEdge, modelNormal, mappedEdge):
        self._inFaceCoordinateSystem = self._getCoordinateSystemForEdge(inEdge, faceNormal)
        self._patchCoordinateSystem = self._getCoordinateSystemForEdge(mappedEdge, modelNormal)

    def mapVertex(self, vertex):
        faceCoords = self._inFaceCoordinateSystem.toLocal(vertex)
        patchCoords = self._patchCoordinateSystem.toGlobal(faceCoords)
        return patchCoords

    def _getCoordinateSystemForEdge(self, edge, normal):
        origin = edge.begin
        e1 = edge.direction.normalized()
        e2 = (e1 ^ normal).normalized()
        return PlaneCoordinateSystem(origin, e1, e2)