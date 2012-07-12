from unittest import TestCase

from pyvi import editor, events, mode, window
from pyvi.modes import insert, normal


class TestNormalMode(TestCase):
    def setUp(self):
        self.editor = editor.Editor()
        self.window = self.editor.active_window
        self.cursor = self.window.cursor
        self.window.insert("foo", "bar", "baz", "quux", "spam", "eggs")

    def keypress(self, keys):
        for key in keys:
            self.editor.keypress(key)

    def test_create_my_cool_motion(self):
        class MyCoolMode(mode.Mode):
            buffer = self.window.buffer
            cursor = self.cursor
            name = "MyCoolMode"
            test_case = self

            @normal.motion
            def keypress_m(self, count):
                return count * 2, count

            @normal.operator
            def keypress_o(self, motion):
                text = self.buffer.chars(start=self.cursor, end=motion)
                self.test_case.text = "".join(text)

        m = self.editor.mode = MyCoolMode(self.editor)

        # Move without an operator
        self.editor.count = 2
        self.keypress("m")
        self.assertEqual(self.cursor.coords, (4, 2))

        # Operate!
        self.cursor.coords = (0, 1)

        self.editor.count = 1
        self.keypress("om")
        self.assertEqual(self.text, "oobarb")

    def test_trimmed(self):
        self.assertEqual(self.cursor.coords, (5, 4))
        self.keypress("jl")
        self.assertEqual(self.cursor.coords, (5, 3))

    def test_basic_movement(self):
        self.keypress("k")
        self.assertEqual(self.cursor.coords, (4, 3))

        self.keypress("j")
        self.assertEqual(self.cursor.coords, (5, 3))

        self.keypress("h")
        self.assertEqual(self.cursor.coords, (5, 2))

        self.keypress("l")
        self.assertEqual(self.cursor.coords, (5, 3))

    def test_basic_movement_with_count(self):
        self.keypress("2k")
        self.assertEqual(self.cursor.coords, (3, 3))

        self.keypress("2j")
        self.assertEqual(self.cursor.coords, (5, 3))

        self.keypress("4h")
        self.assertEqual(self.cursor.coords, (5, 0))

        self.keypress("2l")
        self.assertEqual(self.cursor.coords, (5, 2))

    def test_delete(self):
        coords = self.cursor.coords = (1, 0)
        self.keypress("dl")
        self.assertEqual(self.cursor.coords, coords)
        self.assertEqual(self.window.buffer[1], "ar")
