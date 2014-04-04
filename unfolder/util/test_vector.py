from unittest import TestCase
from unfolder.util.vector import Vector

import numpy.linalg as lg

class TestVector(TestCase):
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

    def test_getItem(self):
        items = (2, 4, 5, 9, 123)
        v1 = Vector(items)

        for index, item in enumerate(items):
            self.assertEqual(item, v1[index])

        v2 = Vector(*items)
        for index, item in enumerate(items):
            self.assertEqual(item, v2[index])