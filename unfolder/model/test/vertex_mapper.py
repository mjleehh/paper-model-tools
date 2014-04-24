from unittest import TestCase
from unfolder.model.edge_proxy import PatchEdgeProxy
from unfolder.model.vertex_mapper import VertexMapper
from unfolder.util.vector import Vector


class VertexMapperTests(TestCase):

    def test_map_displaced(self):
        faceNormal = v(0, 0, 1)
        inEdge = PatchEdgeProxy(v(0, 0, 0), v(19, 0, 0))
        modelNormal = v(0, 0, 1)
        mappedEdge = PatchEdgeProxy(v(2, 3, 1), v(21, 3, 1))
        vm = VertexMapper(faceNormal, inEdge, modelNormal, mappedEdge)

        # begin
        self.assertEqual(vm.mapVertex(v(0, 0, 0)), v(2, 3, 1))
        # on edge
        self.assertEqual(vm.mapVertex(v(3, 0, 0)), v(5, 3, 1))
        # left of edge
        self.assertEqual(vm.mapVertex(v(8, 7, 23)), v(10, 10, 1))
        # right of edge
        self.assertEqual(vm.mapVertex(v(8, -9, 23)), v(10, -6, 1))
        # off plane
        self.assertEqual(vm.mapVertex(v(0, 0, 10)), v(2, 3, 1))

    def test_map_displaced_and_90_degree_z_rotated(self):
        faceNormal = v(0, 0, 1)
        inEdge = PatchEdgeProxy(v(1, 3, -2), v(7, 3, -2))
        modelNormal = v(0, 0, 1)
        mappedEdge = PatchEdgeProxy(v(2, 2, 1), v(2, 8, 1))
        vm = VertexMapper(faceNormal, inEdge, modelNormal, mappedEdge)

        # origin
        self.assertEqual(vm.mapVertex(v(1, 3, -2)), v(2, 2, 1))
        # on edge
        self.assertEqual(vm.mapVertex(v(97, 3, -2)), v(2, 98, 1))
        # left of edge
        self.assertEqual(vm.mapVertex(v(-8, 15, -2)), v(-10, -7, 1))
        # right of edge
        self.assertEqual(vm.mapVertex(v(5, -99, -2)), v(104, 6, 1))
        # outside mapping plane
        self.assertEqual(vm.mapVertex(v(-4, 27, 7)), v(-22, -3, 1))


    def test_map_displaced_and_90_degree_xz_rotated(self):
        faceNormal = v(0, 0, 1)
        inEdge = PatchEdgeProxy(v(2, 3, 0.5), v(2, 12, 0.5))
        modelNormal = v(-1, 0, 0)
        mappedEdge = PatchEdgeProxy(v(-3, 5, -3), v(-3, -22, -3))
        vm = VertexMapper(faceNormal, inEdge, modelNormal, mappedEdge)

        # origin
        self.assertEqual(vm.mapVertex(v(2, 3, 0.5)), v(-3, 5, -3))
        # on edge
        self.assertEqual(vm.mapVertex(v(2, 1, 0.5)), v(-3, 7, -3))
        # left of edge
        self.assertEqual(vm.mapVertex(v(-80, 2, 0.5)), v(-3, 6, 79))
        # right of edge
        self.assertEqual(vm.mapVertex(v(5, 15, 0.5)), v(-3, -7, -6))
        # outside mapping plane
        self.assertEqual(vm.mapVertex(v(0, -4, 9.5)), v(-3, 12, -1))


def v(x, y, z):
    return Vector(float(x), float(y), float(z))