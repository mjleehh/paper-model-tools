from unittest import TestCase, TestSuite
from unfolder.graph.node import Node
from unfolder.tree.knot import Knot, graphToTree
from unfolder.tree.test.sample_trees import createSimpleTree, createPyramidTree


class KnotTester:
    def test_getNames(self):
        expectedNames = set(self.values.keys())

        self.assertEqual(set(self.tree.getNames()), expectedNames)

    def test_structure(self):
        self._traverse(self.tree)

    def _traverse(self, knot):
        values = set([child.value for child in knot])
        self.assertEqual(values, self.values[knot.value])

        for child in knot:
            self._traverse(child)


class SimpleTreeTester(KnotTester, TestCase):
    def setUp(self):
        self.values = {
            'f': {'d', 'a'},
            'd': {'e', 'c'},
            'e': {'b'},
            'b': set(),
            'c': set(),
            'a': {'h', 'g'},
            'h': set(),
            'g': set()}
        self.tree = createSimpleTree()

class PyramidTester(KnotTester, TestCase):
    def setUp(self):
        self.values = {
            'a': {'e', 'd'},
            'e': set(),
            'd': {'c'},
            'c': {'b'},
            'b': set()}
        self.tree = createPyramidTree()