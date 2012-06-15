from unittest import TestCase

import mock

from pyvi.editor import Editor
from pyvi.modes import insert, normal
from pyvi.tests.util import MockCursor


class TestNormalMode(TestCase):
    def setUp(self):
        self.editor = mock.Mock(spec=Editor(), count=None)
        self.window = self.editor.active_window
        self.cursor = self.window.cursor = MockCursor(row=1, column=1)

    def keypress(self, key):
        normal.keypress(self.editor, key)

    def test_count(self):
        self.keypress("2")
        self.assertEqual(self.editor.count, 2)
        self.keypress("3")
        self.assertEqual(self.editor.count, 23)
        self.keypress("8")
        self.assertEqual(self.editor.count, 238)

    def test_h(self):
        self.keypress("h")
        self.assertEqual(self.editor.active_window.cursor.row, 1)
        self.assertEqual(self.editor.active_window.cursor.column, 0)

        self.keypress("1")
        self.keypress("2")
        self.keypress("h")
        self.assertEqual(self.editor.active_window.cursor.row, 1)
        self.assertEqual(self.editor.active_window.cursor.column, -12)

    def test_i(self):
        self.keypress("i")
        self.assertEqual(self.editor.mode, insert)

    def test_j(self):
        self.keypress("j")
        self.assertEqual(self.editor.active_window.cursor.row, 2)
        self.assertEqual(self.editor.active_window.cursor.column, 1)

        self.keypress("2")
        self.keypress("2")
        self.keypress("j")
        self.assertEqual(self.editor.active_window.cursor.row, 24)
        self.assertEqual(self.editor.active_window.cursor.column, 1)

    def test_k(self):
        self.keypress("k")
        self.assertEqual(self.editor.active_window.cursor.row, 0)
        self.assertEqual(self.editor.active_window.cursor.column, 1)

        self.keypress("1")
        self.keypress("7")
        self.keypress("k")
        self.assertEqual(self.editor.active_window.cursor.row, -17)
        self.assertEqual(self.editor.active_window.cursor.column, 1)

    def test_l(self):
        self.keypress("l")
        self.assertEqual(self.editor.active_window.cursor.row, 1)
        self.assertEqual(self.editor.active_window.cursor.column, 2)

        self.keypress("1")
        self.keypress("7")
        self.keypress("l")
        self.assertEqual(self.editor.active_window.cursor.row, 1)
        self.assertEqual(self.editor.active_window.cursor.column, 19)
