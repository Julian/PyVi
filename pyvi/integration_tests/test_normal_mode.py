from unittest import TestCase

from pyvi import editor, events, window
from pyvi.modes import insert, normal


class TestNormalMode(TestCase):
    def setUp(self):
        self.editor = editor.Editor()
        self.window = self.editor.active_window
        self.cursor = self.window.cursor
        self.window.insert("foo", "bar", "baz")

    def test_trimmed(self):
        self.assertEqual(self.cursor.coords, (2, 3))
        self.editor.keypress("j")
        self.editor.keypress("l")
        self.assertEqual(self.cursor.coords, (2, 2))

    def test_basic_movement(self):
        self.editor.keypress("k")
        self.assertEqual(self.cursor.coords, (1, 2))

        self.editor.keypress("j")
        self.assertEqual(self.cursor.coords, (2, 2))

        self.editor.keypress("h")
        self.assertEqual(self.cursor.coords, (2, 1))

        self.editor.keypress("l")
        self.assertEqual(self.cursor.coords, (2, 2))

    def test_basic_movement_with_count(self):
        self.editor.keypress("2")
        self.editor.keypress("k")
        self.assertEqual(self.cursor.coords, (0, 2))

        self.editor.keypress("2")
        self.editor.keypress("j")
        self.assertEqual(self.cursor.coords, (2, 2))

        self.editor.keypress("3")
        self.editor.keypress("h")
        self.assertEqual(self.cursor.coords, (2, 0))

        self.editor.keypress("2")
        self.editor.keypress("l")
        self.assertEqual(self.cursor.coords, (2, 2))
