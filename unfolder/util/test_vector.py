from copy import copy
from unittest import TestCase
from unfolder.util.vector import Vector

import numpy.linalg as lg

class TestVector(TestCase):
    def test_add_2d(self):
        v1 = Vector(1, 2)
        v2 = Vector(77, 12)

        v1plusv2 = Vector(78, 14)
        self.assertEqual(v1 + v2, v1plusv2)

        v3 = copy(v1)
        v3 += v2
        self.assertEqual(v3, v1plusv2)

    def test_add_3d(self):
        v1 = Vector(23, 493, 2)
        v2 = Vector(3, -23, 8)

        v1plusv2 = Vector(26, 470, 10)
        self.assertEqual(v1 + v2, Vector(v1plusv2))

        v3 = copy(v1)
        v3 += v2
        self.assertEqual(v3, v1plusv2)

    def test_add_other_iterable(self):
        v1 = Vector(3, 25, 2, 78)
        v2 = (8, 32, -9, 4)

        v1plusv2 = Vector(11, 57, -7, 82)
        self.assertEqual(v1 + v2, v1plusv2)

        v3 = copy(v1)
        v3 += v2
        self.assertEqual(v3, v1plusv2)

    def test_sub_2d(self):
        v1 = Vector(4, 1, 7)
        v2 = Vector(77, 12, 5)

        v1minusv2 = Vector(-73, -11, 2)
        self.assertEqual(v1 - v2, v1minusv2)

        v3 = copy(v1)
        v3 -= v2
        self.assertEqual(v3, v1minusv2)

    def test_sub_3d(self):
        v1 = Vector(3, 8, 11)
        v2 = (-1, 18, 0)

        v1minusv2 = Vector(4, -10, 11)
        self.assertEqual(v1 - v2, Vector(v1minusv2))

        v3 = copy(v1)
        v3 -= v2
        self.assertEqual(v3, v1minusv2)

    def test_sub_other_iterable(self):
        v1 = Vector(12, 8, 5, 1)
        v2 = (2, 0, 32, -1)

        v1minusv2 = Vector(10, 8, -27, 2)
        self.assertEqual(v1 - v2, v1minusv2)

        v3 = copy(v1)
        v3 -= v2
        self.assertEqual(v3, v1minusv2)

    def test_mul_2d(self):
        v1 = Vector(3, 4)
        v2 = Vector(2, 7)

        v1dotv2 = 34
        self.assertEqual(v1 * v2, v1dotv2)

        v3 = copy(v1)
        v3 *= v2
        self.assertEqual(v3, v1dotv2)

    def test_mul_3d(self):
        v1 = Vector(2, 4, 6)
        v2 = Vector(4, -3, 5)

        v1dotv2 = 26
        self.assertEqual(v1 * v2, v1dotv2)

        v3 = copy(v1)
        v3 *= v2
        self.assertEqual(v3, v1dotv2)

    def test_mul_other_iterable(self):
        v1 = Vector(2, -3, 9, 8)
        v2 = (2, 0, 7, -5)

        v1dotv2 = 27
        self.assertEqual(v1 * v2, v1dotv2)

        v3 = copy(v1)
        v3 *= v2
        self.assertEqual(v3, v1dotv2)

    def test_div(self):
        v1 = Vector(3, 1)
        s1 = 7
        v1overs1 = Vector(21, 7)
        self.assertEqual(v1 / s1, v1overs1)

        v3 = copy(v1)
        v3 /=  s1
        self.assertEqual(v3, v1overs1)

    def test_crossProduct(self):
        v1 = Vector(1, 0, 0)

        v2 = Vector(0, 1, 0)
        v1xv2 = Vector(0, 0, 1)
        self.assertEqual(v1 ^ v2, v1xv2)

        v3 = copy(v1)
        v3 ^= v2
        self.assertEqual(v3, v1xv2)

        v2xv1 = Vector(0, 0, -1)
        self.assertEqual(v2 ^ v1, v2xv1)
        v4 = copy(v2)
        v4 ^= v1
        self.assertEqual(v4, v2xv1)

    def test_normalize(self):
        v = Vector(2., 5., 8., 5.)
        v.normalize()
        self.assertEqual(v.norm(), 1.)

    def test_norm(self):
        v1 = Vector(1., 0.)
        self.assertEqual(v1.norm(), 1.)

        v2Coords = (1., 3., 19.)
        v2 = Vector(v2Coords)
        self.assertEqual(v2.norm(), lg.norm(v2Coords))

    def test_equal(self):
        v1 = Vector(1, 2, 4)
        v2 = Vector(2, 7, 8)
        v3 = Vector(1, 2, 4)

        self.assertTrue(v1 != v2)
        self.assertFalse(v1 == v2)

        self.assertTrue(v1 == v3)
        self.assertFalse(v1 != v3)

    def test_getItem(self):
        items = (2, 4, 5, 9, 123)
        v1 = Vector(items)

        for index, item in enumerate(items):
            self.assertEqual(item, v1[index])

        v2 = Vector(*items)
        for index, item in enumerate(items):
            self.assertEqual(item, v2[index])

    def test_len(self):
        v1 = Vector(1)
        self.assertEqual(len(v1), 1)

        v2 = Vector(1, 2)
        self.assertEqual(len(v2), 2)

        v3 = Vector(1, 2, 3)
        self.assertEqual(len(v3), 3)

        v4 = Vector(1, 2, 3, 4)
        self.assertEqual(len(v4), 4)
