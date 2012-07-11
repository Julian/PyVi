import unittest

import mock

from pyvi.editor import Editor


class MockCursor(mock.Mock):
    column = 0
    row = 0

    def __iter__(self):
        return iter([self.row, self.column])

    @property
    def coords(self):
        return self.row, self.column

    @coords.setter
    def coords(self, coords):
        self.row, self.column = coords


class ModeTest(unittest.TestCase):
    def setUp(self):
        self.editor = mock.Mock(spec=Editor(), count=None)
        self.window = self.editor.active_window
        self.cursor = self.window.cursor = MockCursor()
        self.mode = self.Mode(self.editor)

    def keypress(self, *keys):
        for key in keys:
            self.mode.keypress(key)
