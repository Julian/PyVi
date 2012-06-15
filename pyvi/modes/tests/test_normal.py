from unittest import TestCase

import mock

from pyvi.editor import Editor
from pyvi.modes import insert, normal
from pyvi.tests.util import MockCursor


class TestNormalMode(TestCase):
    def setUp(self):
        self.editor = mock.Mock(spec=Editor())
        self.editor.active_window.cursor = MockCursor(row=1, column=1)

    def keypress(self, key):
        normal.keypress(self.editor, key)

    def test_h(self):
        self.keypress("h")
        self.assertEqual(self.editor.active_window.cursor.row, 1)
        self.assertEqual(self.editor.active_window.cursor.column, 0)

    def test_i(self):
        self.keypress("i")
        self.assertEqual(self.editor.mode, insert)

    def test_j(self):
        self.keypress("j")
        self.assertEqual(self.editor.active_window.cursor.row, 2)
        self.assertEqual(self.editor.active_window.cursor.column, 1)

    def test_k(self):
        self.keypress("k")
        self.assertEqual(self.editor.active_window.cursor.row, 0)
        self.assertEqual(self.editor.active_window.cursor.column, 1)

    def test_l(self):
        self.keypress("l")
        self.assertEqual(self.editor.active_window.cursor.row, 1)
        self.assertEqual(self.editor.active_window.cursor.column, 2)
