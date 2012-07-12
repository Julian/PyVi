from unittest import TestCase

import mock

from pyvi.modes.insert import Insert
from pyvi.modes.normal import Normal
from pyvi.tests.util import MockCursor, ModeTest


class TestNormalMode(ModeTest):

    Mode = Normal

    def setUp(self):
        super(TestNormalMode, self).setUp()
        self.cursor.coords = (1, 1)

    def test_count(self):
        self.keypress("2")
        self.assertEqual(self.editor.count, 2)
        self.keypress("3")
        self.assertEqual(self.editor.count, 23)
        self.keypress("8")
        self.assertEqual(self.editor.count, 238)

    def test_d(self):
        self.keypress("dl")
        self.assertEqual(self.cursor.coords, (1, 1))
        self.window.delete.assert_called_once_with(end=(1, 2))

    def test_h(self):
        self.keypress("h")
        self.assertEqual(self.cursor.coords, (1, 0))

        self.keypress("12h")
        self.assertEqual(self.cursor.coords, (1, -12))

    def test_i(self):
        self.keypress("i")
        self.assertEqual(self.editor.mode.name, "insert")

    def test_j(self):
        self.keypress("j")
        self.assertEqual(self.cursor.coords, (2, 1))

        self.keypress("22j")
        self.assertEqual(self.cursor.coords, (24, 1))

    def test_k(self):
        self.keypress("k")
        self.assertEqual(self.cursor.coords, (0, 1))

        self.keypress("17k")
        self.assertEqual(self.cursor.coords, (-17, 1))

    def test_l(self):
        self.keypress("l")
        self.assertEqual(self.cursor.coords, (1, 2))

        self.keypress("17l")
        self.assertEqual(self.cursor.coords, (1, 19))
