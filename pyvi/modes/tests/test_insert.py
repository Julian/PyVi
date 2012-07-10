from unittest import TestCase

import mock

from pyvi.editor import Editor
from pyvi.modes import insert
from pyvi.tests.util import MockCursor


class TestInsertMode(TestCase):
    def setUp(self):
        self.editor = mock.Mock(spec=Editor())
        self.cursor = self.editor.active_window.cursor = MockCursor(
            row=0, column=1
        )
        self.mode = insert.Insert(self.editor)

    def keypress(self, key):
        self.mode.keypress(key)

    def test_esc(self):
        self.assertEqual(self.cursor.coords, (0, 1))
        self.keypress(u"esc")
        self.assertEqual(self.editor.mode, self.editor.Normal(self.editor))
        self.assertEqual(self.cursor.coords, (0, 0))

    def test_inserts_characters(self):
        self.keypress(u"f")
        self.editor.active_window.insert.assert_called_once_with(u"f")
        self.keypress(u"/")
        self.editor.active_window.insert.assert_called_with(u"/")

    def test_insert_tab(self):
        self.keypress(u"tab")
        self.editor.active_window.insert.assert_called_once_with(u"\t")

    def test_insert_nontext(self):
        self.keypress(u"enter")
        self.editor.active_window.insert.assert_called_once_with(u"", u"")
