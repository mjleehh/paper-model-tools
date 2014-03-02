from coordinatesystem import CoordinateSystem


def getMinimumSurfaceAreaForGeometry(mappingPlaneNormal, vertices):
    def getAreaForRect(vertex1, vertex2, vertices):
        e1 = vertex2 - vertex1
        e1.normalize()
        e2 = e1 ^ mappingPlaneNormal
        e2.nomalize()

        coordinateSystem = CoordinateSystem(vertex1, e1, e2)
        for vertex in vertices:
            coordinateSystem.toLocal(vertex)


    for i, vertex1 in enumerate(vertices):
        for vertex2 in vertices[i + 1:]:
            print(vertex1, vertex2)

